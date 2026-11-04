(() => {
    const section = document.getElementById('skills');
    if (!section) return;

    const config = section.dataset;
    const searchForm = document.getElementById('skill-search-form');
    const searchInput = document.getElementById('skill-search-input');
    const categoryInput = document.getElementById('skill-category');
    const grid = document.getElementById('skills-grid');
    const loading = document.getElementById('skills-loading');
    const empty = document.getElementById('skills-empty');
    const error = document.getElementById('skills-error');
    const csrfToken = section.querySelector('[name="csrfmiddlewaretoken"]').value;
    const dummyId = '00000000-0000-0000-0000-000000000000';
    let controller;
    let debounceTimer;

    // textContent menjaga data JSON sebagai teks, bukan HTML aktif.
    function element(tag, className, text) {
        const node = document.createElement(tag);
        node.className = className;
        if (text !== undefined) node.textContent = text;
        return node;
    }

    function itemUrl(template, id) {
        return template.replace(dummyId, encodeURIComponent(id));
    }

    function buildCard(item) {
        const skill = item;
        const card = element('article', 'experience-card');
        if (skill.icon_url) {
            // Batasi protokol URL, termasuk untuk data lama yang tersimpan.
            try {
                const url = new URL(skill.icon_url);
                if (['http:', 'https:'].includes(url.protocol)) {
                    const image = element('img', 'skill-icon');
                    image.src = url.href;
                    image.alt = `Ikon ${skill.name}`;
                    card.append(image);
                }
            } catch { /* URL tidak valid tidak ditampilkan. */ }
        }
        card.append(element('span', 'experience-category', skill.category_display));
        if (skill.is_featured) card.append(element('span', 'skill-badge', 'Unggulan'));
        card.append(element('h2', '', skill.name));
        if (skill.description) card.append(element('p', 'experience-description', skill.description));
        const level = element('p', 'skill-level', '★'.repeat(skill.proficiency) + '☆'.repeat(5 - skill.proficiency));
        level.setAttribute('aria-label', `Level ${skill.proficiency} dari 5`);
        level.append(element('span', '', skill.proficiency_display));
        card.append(level);

        const actions = element('div', 'project-actions');
        const starLabel = skill.is_starred ? 'Unstar' : 'Star';
        const star = element(config.authenticated === 'true' ? 'button' : 'a',
            `button button-star${skill.is_starred ? ' is-starred' : ''}`, `★ ${starLabel} `);
        star.append(element('span', 'star-count', skill.star_count));
        if (config.authenticated === 'true') {
            star.type = 'button';
            star.title = skill.starred_by_names || 'Jadilah yang pertama memberi star';
            star.addEventListener('click', async () => {
                if (star.disabled) return;
                star.disabled = true;
                try {
                    await writeSkill(itemUrl(config.starUrl, skill.id), 'POST');
                    showToast('Berhasil', 'Star diperbarui.', 'success');
                    await fetchSkills();
                } catch (err) {
                    showToast('Gagal', err.message, 'error');
                } finally { star.disabled = false; }
            });
            actions.append(star);
        } else {
            star.href = config.loginUrl;
            star.title = 'Login untuk memberi star';
            actions.append(star);
        }
        if (config.canEdit === 'true') {
            const edit = element('a', 'button button-secondary', 'Edit');
            edit.href = itemUrl(config.editUrl, item.id);
            actions.append(edit);
        }
        if (config.canDelete === 'true') {
            const remove = element('button', 'button button-danger', 'Hapus Skill');
            remove.type = 'button';
            remove.addEventListener('click', () => {
                document.getElementById('delete-skill-name').textContent = skill.name;
                document.getElementById('delete-skill-form').action = itemUrl(config.deleteUrl, item.id);
                document.getElementById('delete-skill-modal').showPopover();
            });
            actions.append(remove);
        }
        card.append(actions);
        return card;
    }

    function display(state) {
        loading.classList.toggle('hide', state !== 'loading');
        empty.classList.toggle('hide', state !== 'empty');
        error.classList.toggle('hide', state !== 'error');
        grid.classList.toggle('hide', state !== 'grid');
        grid.setAttribute('aria-busy', String(state === 'loading'));
    }

    async function fetchSkills() {
        controller?.abort();
        const currentController = new AbortController();
        controller = currentController;
        display('loading');
        const params = new URLSearchParams({ name: searchInput.value.trim(), category: categoryInput.value });
        try {
            const response = await fetch(`${config.listUrl}?${params}`, {
                headers: { Accept: 'application/json' }, signal: currentController.signal,
            });
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            const data = await response.json();
            if (currentController.signal.aborted) return;
            grid.replaceChildren(...data.map(buildCard));
            empty.textContent = params.get('name') || params.get('category')
                ? 'Tidak ada skill yang cocok dengan filter tersebut.'
                : 'Belum ada skill yang ditambahkan.';
            display(data.length ? 'grid' : 'empty');
        } catch (err) {
            if (err.name === 'AbortError') return;
            display('error');
        }
    }

    function searchNow() {
        clearTimeout(debounceTimer);
        fetchSkills();
    }
    searchInput.addEventListener('input', () => {
        clearTimeout(debounceTimer);
        controller?.abort();
        debounceTimer = setTimeout(fetchSkills, 300);
    });
    categoryInput.addEventListener('change', searchNow);
    searchForm.addEventListener('submit', event => {
        event.preventDefault();
        searchNow();
    });
    document.getElementById('skills-retry').addEventListener('click', searchNow);

    function errorMessage(data) {
        if (Array.isArray(data)) return data.map(errorMessage).join(' ');
        if (data && typeof data === 'object') {
            return Object.entries(data).map(([key, value]) => `${key}: ${errorMessage(value)}`).join(' ');
        }
        return String(data ?? '');
    }

    async function writeSkill(url, method, payload) {
        const response = await fetch(url, {
            method, credentials: 'same-origin',
            headers: { Accept: 'application/json', 'Content-Type': 'application/json', 'X-CSRFToken': csrfToken },
            body: payload === undefined ? undefined : JSON.stringify(payload),
        });
        if (response.status === 204) return null;
        const data = await response.json().catch(() => null);
        if (!response.ok) throw new Error(errorMessage(data) || `HTTP ${response.status}`);
        return data;
    }

    const deleteForm = document.getElementById('delete-skill-form');
    deleteForm?.addEventListener('submit', async event => {
        event.preventDefault();
        const button = deleteForm.querySelector('[type="submit"]');
        if (button.disabled) return;
        button.disabled = true;
        try {
            await writeSkill(deleteForm.action, 'DELETE');
            document.getElementById('delete-skill-modal').hidePopover();
            showToast('Berhasil', 'Skill dihapus.', 'success');
            await fetchSkills();
        } catch (err) { showToast('Gagal menghapus skill', err.message, 'error'); }
        finally { button.disabled = false; }
    });

    // Modal tambah hanya tersedia bagi pemilik portofolio.
    const form = document.getElementById('skill-form');
    if (form) {
        form.addEventListener('submit', async event => {
            event.preventDefault();
            const submit = form.querySelector('[type="submit"]');
            if (submit.disabled) return;
            submit.disabled = true;
            submit.textContent = 'Menyimpan...';
            try {
                const payload = Object.fromEntries(new FormData(form));
                delete payload.csrfmiddlewaretoken;
                payload.is_featured = form.elements.is_featured.checked;
                payload.proficiency = Number(payload.proficiency);
                await writeSkill(config.listUrl, 'POST', payload);
                form.reset();
                document.getElementById('add-skill-modal').hidePopover();
                showToast('Berhasil', 'Skill ditambahkan.', 'success');
                searchNow();
            } catch (err) {
                showToast('Gagal menambahkan skill', err.message, 'error');
            } finally {
                submit.disabled = false;
                submit.textContent = 'Tambah Skill';
            }
        });
    }
    fetchSkills();
})();

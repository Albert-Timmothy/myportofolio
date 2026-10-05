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
        const skill = item.fields;
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
            const form = element('form', 'star-form');
            form.method = 'post';
            form.action = itemUrl(config.starUrl, item.pk);
            const token = element('input', '');
            token.type = 'hidden';
            token.name = 'csrfmiddlewaretoken';
            token.value = csrfToken;
            star.type = 'submit';
            form.append(token, star);
            actions.append(form);
        } else {
            star.href = config.loginUrl;
            star.title = 'Login untuk memberi star';
            actions.append(star);
        }
        if (config.canEdit === 'true') {
            const edit = element('a', 'button button-secondary', 'Edit');
            edit.href = itemUrl(config.editUrl, item.pk);
            actions.append(edit);
        }
        if (config.canDelete === 'true') {
            const remove = element('button', 'button button-danger', 'Hapus Skill');
            remove.type = 'button';
            remove.addEventListener('click', () => {
                document.getElementById('delete-skill-name').textContent = skill.name;
                document.getElementById('delete-skill-form').action = itemUrl(config.deleteUrl, item.pk);
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
        debounceTimer = setTimeout(fetchSkills, 300);
    });
    categoryInput.addEventListener('change', searchNow);
    searchForm.addEventListener('submit', event => {
        event.preventDefault();
        searchNow();
    });
    document.getElementById('skills-retry').addEventListener('click', searchNow);

    // Modal hanya ada bagi pengguna dengan permission add_skill.
    const form = document.getElementById('skill-form');
    if (form) {
        form.addEventListener('submit', async event => {
            event.preventDefault();
            const submit = form.querySelector('[type="submit"]');
            if (submit.disabled) return;
            submit.disabled = true;
            submit.textContent = 'Menyimpan...';
            try {
                const response = await fetch(form.action, {
                    method: 'POST', body: new FormData(form), headers: { Accept: 'application/json' },
                });
                const result = await response.json();
                if (!response.ok) {
                    const messages = result.errors
                        ? Object.values(result.errors).flat().map(err => err.message)
                        : [result.message || 'Skill gagal ditambahkan. Silakan coba lagi.'];
                    showToast('Gagal menambahkan skill', messages.join(' '), 'error');
                    return;
                }
                form.reset();
                document.getElementById('add-skill-modal').hidePopover();
                showToast('Berhasil', result.message, 'success');
                // Bersihkan filter agar skill baru langsung terlihat.
                searchInput.value = '';
                categoryInput.value = '';
                searchNow();
            } catch {
                showToast('Gagal menambahkan skill', 'Tidak dapat menghubungi server. Silakan coba lagi.', 'error');
            } finally {
                submit.disabled = false;
                submit.textContent = 'Tambah Skill';
            }
        });
    }
    fetchSkills();
})();

(() => {
    const grid = document.getElementById('grid');
    const searchInput = document.getElementById('search-input');
    const searchForm = document.getElementById('project-search-form');
    const projectForm = document.getElementById('project-form');
    const csrfToken = document.querySelector('[name="csrfmiddlewaretoken"]').value;
    const dummyId = '00000000-0000-0000-0000-000000000000';
    let controller;
    let debounceTimer;

    function element(tag, className, text) {
        const node = document.createElement(tag);
        node.className = className;
        if (text !== undefined) node.textContent = text;
        return node;
    }

    function endpoint(template, id) {
        return template.replace(dummyId, encodeURIComponent(id));
    }

    function safeUrl(value) {
        try {
            const url = new URL(value);
            return ['http:', 'https:'].includes(url.protocol) ? url.href : '';
        } catch { return ''; }
    }

    function display(state) {
        for (const name of ['loading', 'error', 'empty', 'grid']) {
            document.getElementById(name).classList.toggle('hide', name !== state);
        }
        grid.setAttribute('aria-busy', String(state === 'loading'));
    }

    function buildCard(project) {
        const card = element('article', 'experience-card');
        const imageUrl = safeUrl(project.project_image_url);
        if (imageUrl) {
            const image = element('img', 'project-image');
            image.src = imageUrl;
            image.alt = `Gambar ${project.title}`;
            card.append(image);
        }
        // Data pengguna selalu menjadi teks, termasuk data lama di database.
        card.append(
            element('h2', '', project.title),
            element('span', 'experience-category', project.tech_stack),
            element('p', 'experience-description', project.description),
        );
        const actions = element('div', 'project-actions');
        const projectUrl = safeUrl(project.project_url);
        if (projectUrl) {
            const link = element('a', 'button', 'Lihat Project');
            link.href = projectUrl;
            actions.append(link);
        }
        const star = element(IS_AUTHENTICATED ? 'button' : 'a',
            `button button-star${project.is_starred ? ' is-starred' : ''}`,
            `★ ${project.is_starred ? 'Unstar' : 'Star'} `);
        star.append(element('span', 'star-count', project.star_count));
        star.title = project.starred_by_names || 'Jadilah yang pertama memberi star';
        if (IS_AUTHENTICATED) {
            star.type = 'button';
            star.dataset.action = 'star';
            star.dataset.id = project.id;
        } else {
            star.href = LOGIN_URL;
            star.title = 'Login untuk memberi star';
        }
        actions.append(star);
        if (CAN_EDIT) {
            const edit = element('a', 'button button-secondary', 'Edit');
            edit.href = endpoint(EDIT_PROJECT_ENDPOINT, project.id);
            actions.append(edit);
        }
        if (CAN_DELETE) {
            const remove = element('button', 'button button-danger', 'Hapus');
            remove.type = 'button';
            remove.dataset.action = 'delete';
            remove.dataset.id = project.id;
            actions.append(remove);
        }
        const wrapper = element('div', 'project-card-actions');
        wrapper.append(actions);
        card.append(wrapper);
        return card;
    }

    async function fetchProjects() {
        controller?.abort();
        const current = new AbortController();
        controller = current;
        display('loading');
        const params = new URLSearchParams({ title: searchInput.value.trim() });
        try {
            const response = await fetch(`${BASE_PROJECTS_ENDPOINT}?${params}`, {
                headers: { Accept: 'application/json' }, signal: current.signal,
            });
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            const data = await response.json();
            if (current.signal.aborted) return;
            grid.replaceChildren(...data.map(buildCard));
            display(data.length ? 'grid' : 'empty');
        } catch (error) {
            if (error.name !== 'AbortError') display('error');
        }
    }

    function errorMessage(data) {
        if (Array.isArray(data)) return data.map(errorMessage).join(' ');
        if (data && typeof data === 'object') {
            return Object.entries(data).map(([key, value]) => `${key}: ${errorMessage(value)}`).join(' ');
        }
        return String(data ?? '');
    }

    async function writeProject(url, method, payload) {
        const response = await fetch(url, {
            method,
            credentials: 'same-origin',
            headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: payload === undefined ? undefined : JSON.stringify(payload),
        });
        if (response.status === 204) return null;
        const data = await response.json().catch(() => null);
        if (!response.ok) throw new Error(errorMessage(data) || `HTTP ${response.status}`);
        return data;
    }

    projectForm?.addEventListener('submit', async event => {
        event.preventDefault();
        const button = projectForm.querySelector('[type="submit"]');
        if (button.disabled) return;
        button.disabled = true;
        const payload = Object.fromEntries(new FormData(projectForm));
        delete payload.csrfmiddlewaretoken;
        try {
            await writeProject(BASE_PROJECTS_ENDPOINT, 'POST', payload);
            projectForm.reset();
            document.getElementById('add-project-modal').hidePopover();
            showToast('Berhasil', 'Proyek berhasil ditambahkan.', 'success');
            await fetchProjects();
        } catch (error) {
            showToast('Gagal menambahkan proyek', error.message, 'error');
        } finally {
            button.disabled = false;
        }
    });

    grid.addEventListener('click', async event => {
        const button = event.target.closest('button[data-action]');
        if (!button || button.disabled) return;
        const isDelete = button.dataset.action === 'delete';
        if (isDelete && !confirm('Yakin ingin menghapus proyek ini?')) return;
        button.disabled = true;
        try {
            await writeProject(
                endpoint(isDelete ? DETAIL_PROJECT_ENDPOINT : STAR_PROJECT_ENDPOINT, button.dataset.id),
                isDelete ? 'DELETE' : 'POST',
            );
            showToast('Berhasil', isDelete ? 'Proyek dihapus.' : 'Star diperbarui.', 'success');
            await fetchProjects();
        } catch (error) {
            showToast('Permintaan gagal', error.message, 'error');
        } finally {
            button.disabled = false;
        }
    });

    searchInput.addEventListener('input', () => {
        clearTimeout(debounceTimer);
        controller?.abort();
        debounceTimer = setTimeout(fetchProjects, 300);
    });
    searchForm.addEventListener('submit', event => {
        event.preventDefault();
        clearTimeout(debounceTimer);
        fetchProjects();
    });
    fetchProjects();
})();

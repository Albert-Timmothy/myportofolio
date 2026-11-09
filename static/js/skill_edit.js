(() => {
    const form = document.getElementById('skill-edit-form');
    if (!form) return;

    function errorMessage(data) {
        if (Array.isArray(data)) return data.map(errorMessage).join(' ');
        if (data && typeof data === 'object') {
            return Object.entries(data).map(([key, value]) => `${key}: ${errorMessage(value)}`).join(' ');
        }
        return String(data ?? '');
    }

    form.addEventListener('submit', async event => {
        event.preventDefault();
        const button = form.querySelector('[type="submit"]');
        if (button.disabled) return;
        button.disabled = true;
        const label = button.textContent;
        button.textContent = 'Menyimpan...';
        try {
            const payload = Object.fromEntries(new FormData(form));
            const csrfToken = payload.csrfmiddlewaretoken;
            delete payload.csrfmiddlewaretoken;
            payload.is_featured = form.elements.is_featured.checked;
            payload.proficiency = Number(payload.proficiency);
            const response = await fetch(form.dataset.apiUrl, {
                method: 'PATCH', credentials: 'same-origin',
                headers: {
                    Accept: 'application/json', 'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken,
                },
                body: JSON.stringify(payload),
            });
            const data = await response.json().catch(() => null);
            if (!response.ok) throw new Error(errorMessage(data) || `HTTP ${response.status}`);
            // Gunakan hasil validasi server tanpa memuat ulang halaman.
            for (const field of ['name', 'category', 'proficiency', 'description', 'icon_url']) {
                form.elements[field].value = data[field];
            }
            form.elements.is_featured.checked = data.is_featured;
            showToast('Berhasil', 'Skill berhasil diperbarui.', 'success');
        } catch (error) {
            showToast('Gagal memperbarui skill', error.message, 'error');
        } finally {
            button.disabled = false;
            button.textContent = label;
        }
    });
})();

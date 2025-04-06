"use strict";

document.addEventListener('DOMContentLoaded', function () {
    const logoutBtn = document.getElementById('logoutBtn');

    if (logoutBtn) {
        logoutBtn.addEventListener('click', function (event) {
            event.preventDefault();

            const logoutUrl = logoutBtn.dataset.logoutUrl;
            const csrfToken = logoutBtn.dataset.csrfToken;

            const form = document.createElement('form');
            form.method = 'POST';
            form.action = logoutUrl;

            const csrfInput = document.createElement('input');
            csrfInput.type = 'hidden';
            csrfInput.name = 'csrfmiddlewaretoken';
            csrfInput.value = csrfToken;

            form.appendChild(csrfInput);
            document.body.appendChild(form);
            form.submit();
        });
    }
});


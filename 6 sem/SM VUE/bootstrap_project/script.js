class FormcarrySubmitter {
    constructor(formElement, options = {}) {
        this.form = formElement;
        this.endpoint = options.endpoint || 'https://formcarry.com/s/QiUdEb9NdK';
        this.submitButton = this.form.querySelector('button[type="submit"]');
        this.originalButtonText = this.submitButton.textContent;
        this.abortController = null;
        this.timeoutId = null;

        this.messageContainer = document.createElement('div');
        this.messageContainer.className = 'form-message';
        this.form.appendChild(this.messageContainer);

        this.bindEvents();
    }

    bindEvents() {
        this.form.addEventListener('submit', (e) => this.handleSubmit(e));
    }

    async handleSubmit(event) {
        event.preventDefault();
        this.resetMessages();
        this.disableSubmitButton('Отправка...');

        this.abortController = new AbortController();

        this.timeoutId = setTimeout(() => {
            this.abortController.abort();
            this.showError('Превышено время ожидания ответа сервера');
            this.enableSubmitButton();
        }, 10000);

        try {
            const formData = new FormData(this.form);
            const response = await fetch(this.endpoint, {
                method: 'POST',
                body: formData,
                signal: this.abortController.signal,
                headers: {
                    'Accept': 'application/json'
                }
            });

            clearTimeout(this.timeoutId);

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();

            if (data.status === 'success') {
                this.showSuccess('Форма успешно отправлена!');
                this.form.reset();
            } else {
                this.showError(data.message || 'Произошла ошибка при отправке формы');
            }
        } catch (error) {
            clearTimeout(this.timeoutId);

            if (error.name === 'AbortError') {
                console.log('Fetch aborted');
            } else {
                this.showError(`Ошибка: ${error.message}`);
                console.error('Error:', error);
            }
        } finally {
            this.enableSubmitButton();
            this.abortController = null;
            this.timeoutId = null;
        }
    }

    disableSubmitButton(text) {
        this.submitButton.disabled = true;
        this.submitButton.textContent = text || 'Отправка...';

        if (!this.cancelButton) {
            this.cancelButton = document.createElement('button');
            this.cancelButton.type = 'button';
            this.cancelButton.textContent = 'Отменить';
            this.cancelButton.className = 'btn btn-secondary ms-2';
            this.cancelButton.addEventListener('click', () => this.cancelSubmit());
            this.submitButton.insertAdjacentElement('afterend', this.cancelButton);
        }
    }

    enableSubmitButton() {
        this.submitButton.disabled = false;
        this.submitButton.textContent = this.originalButtonText;

        if (this.cancelButton) {
            this.cancelButton.remove();
            this.cancelButton = null;
        }
    }

    cancelSubmit() {
        if (this.abortController) {
            this.abortController.abort();
            this.showError('Отправка формы отменена');
        }
        if (this.timeoutId) {
            clearTimeout(this.timeoutId);
            this.timeoutId = null;
        }
        this.enableSubmitButton();
    }

    showSuccess(message) {
        this.messageContainer.innerHTML = `
      <div class="alert alert-success alert-dismissible fade show" role="alert">
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
      </div>
    `;
    }

    showError(message) {
        this.messageContainer.innerHTML = `
      <div class="alert alert-danger alert-dismissible fade show" role="alert">
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
      </div>
    `;
    }

    resetMessages() {
        this.messageContainer.innerHTML = '';
    }
}

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('datePicker').valueAsDate = new Date();

    const form = document.querySelector('form');
    if (form) {
        new FormcarrySubmitter(form, {
            endpoint: 'https://formcarry.com/s/QiUdEb9NdK'
        });
    }
});
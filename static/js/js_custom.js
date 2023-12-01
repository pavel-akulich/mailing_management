document.addEventListener("DOMContentLoaded", function () {
    // Автоматическое закрытие сообщений через 4 секунды
    setTimeout(function () {
        let messages = document.querySelectorAll('.message');
        messages.forEach(function (message) {
            message.style.display = 'none';
        });
    }, 4000);

    // Закрытие сообщения при клике на крестик
    let closeButtons = document.querySelectorAll('.close-btn');
    closeButtons.forEach(function (btn) {
        btn.addEventListener('click', function () {
            let message = this.closest('.message');
            message.style.display = 'none';
        });
    });
});
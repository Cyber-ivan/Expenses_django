document.addEventListener('DOMContentLoaded', () => {
    const tabs = document.querySelectorAll('.tab');
    const tabContents = document.querySelectorAll('.tab-content');
    const groupSelect = document.getElementById('group-select');
    const groupExpensesBody = document.getElementById('group-expenses-body');
    const participantFilters = document.querySelectorAll('.participant-filter');
    const filterForm = document.getElementById('filter-form');
    const selectedParticipantsInput = document.getElementById('selected_participants');

    // Переключение вкладок
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            tabs.forEach(t => t.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));
            tab.classList.add('active');
            document.getElementById(tab.dataset.tab).classList.add('active');
        });
    });

    // Фильтрация расходов по группе
    groupSelect.addEventListener('change', () => {
        const selectedGroupId = groupSelect.value;
        const rows = groupExpensesBody.querySelectorAll('tr');
        rows.forEach(row => {
            row.style.display = row.dataset.groupId === selectedGroupId ? '' : 'none';
        });
    });

    // Обработка изменения состояния чекбоксов
    participantFilters.forEach(filter => {
        filter.addEventListener('change', () => {
            const selectedUserIds = Array.from(participantFilters)
                .filter(f => f.checked)
                .map(f => f.value);

            selectedParticipantsInput.value = selectedUserIds.join(',');

            // Отправка формы на сервер
            filterForm.submit();
        });
    });

    // Применение фильтров при загрузке страницы
    const selectedParticipants = selectedParticipantsInput.value.split(',');
    participantFilters.forEach(filter => {
        if (selectedParticipants.includes(filter.value)) {
            filter.checked = true;
        }
    });
});
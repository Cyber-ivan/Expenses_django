        document.addEventListener('DOMContentLoaded', () => {
            const tabs = document.querySelectorAll('.tab');
            const tabContents = document.querySelectorAll('.tab-content');
            const groupSelect = document.getElementById('group-select');
            const groupExpensesBody = document.getElementById('group-expenses-body');

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
        });
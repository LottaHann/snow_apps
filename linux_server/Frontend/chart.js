       // Funktion för att läsa data från localStorage
       function readData() {
        let allData = localStorage.getItem('pageData');
        if (allData === null) {
            return [];
        } else {
            return JSON.parse(allData);
        }
    }

    // Funktion för att rendera data i tabellen
    function renderTable(data) {
        const tableBody = document.getElementById('data-table').querySelector('tbody');
        tableBody.innerHTML = ''; // Rensa befintligt innehåll

        data.forEach(item => {
            const row = document.createElement('tr');

            const idCell = document.createElement('td');
            idCell.textContent = item.id;
            row.appendChild(idCell);

            const pageCell = document.createElement('td');
            pageCell.textContent = item.page;
            row.appendChild(pageCell);

            const timeCell = document.createElement('td');
            timeCell.textContent = item.time;
            row.appendChild(timeCell);

            tableBody.appendChild(row);
        });
    }

    // Läsa data från localStorage och rendera tabellen
    const data = readData();
    renderTable(data);
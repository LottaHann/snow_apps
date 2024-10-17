// Funktion för att generera ett nytt ID
function generateId() {
  let lastId = localStorage.getItem('lastId');
  if (lastId === null) {
      lastId = 0;
  } else {
      lastId = parseInt(lastId);
  }
  const newId = lastId + 1;
  localStorage.setItem('lastId', newId);
  return newId;
}

// Funktion för att spara data i localStorage
function saveData(pageNumber, timeSpent) {
  const id = generateId();
  const data = {
      id: id,
      page: pageNumber,
      time: timeSpent
  };

  // Hämta befintlig data från localStorage
  let allData = localStorage.getItem('pageData');
  if (allData === null) {
      allData = [];
  } else {
      allData = JSON.parse(allData);
  }

  // Lägg till ny data
  allData.push(data);

  // Spara tillbaka till localStorage
  localStorage.setItem('pageData', JSON.stringify(allData));
}

// Funktion för att omvandla millisekunder till ett läsbart format
function formatTime(ms) {
  const minutes = Math.floor(ms / 6000) / 10;
  return `${minutes} min`;
}

// Funktion för att få sidnummer baserat på URL
function getPageNumber() {
  const path = window.location.pathname;
  switch (path) {
      case '/contact/':
          return "Talk app";
      case '/info/':
          return "Text app";
      case '/arcada/':
          return "Swaps Face app";
      case '/techlabs/':
          return "Statistics app";
      default:
          return 0; // Om sidan inte är igenkänd
  }
}

// Starttid
const startTime = Date.now();

// Få sidnummer från URL
const pageNumber = getPageNumber();

// När användaren lämnar sidan
window.addEventListener('beforeunload', () => {
  const endTime = Date.now();
  const timeSpent = endTime - startTime;
  const formattedTime = formatTime(timeSpent);
  saveData(pageNumber, formattedTime);
});

// För att läsa data från localStorage
function readData() {
  let allData = localStorage.getItem('pageData');
  if (allData === null) {
      return [];
  } else {
      return JSON.parse(allData);
  }
}

readData();
// Exempel på att läsa data

console.log(window.location.pathname);

console.log(readData());

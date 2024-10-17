// efter contact then selected person structure:
//  generated the person's HTML structure:
function createPersonCard(name, title, imagePath, summary, publications) {
    return `
        <div class="col-md-6">
            <div class="css-165ep0a">
                <h1 class="css-1ykowef">${name}</h1>
                <p class="css-1i9vogi">${title}</p>
                <div class="css-1yjt3jx">
                    <div class="col mt-5 d-flex justify-content-left">
                        <div class="btn-group rounded-circle" style="margin-bottom: 20px;">
                            <div class="position-relative rounded-circle bg-primary d-flex align-items-end justify-content-center"
                                style="width: 200px; height: 200px; padding-bottom: 40px;">
                                <a href="#" class="text-decoration-none">
                                    <img src="${imagePath}" alt="Circle Image"
                                        class="rounded-circle position-absolute top-50 start-50 translate-middle"
                                        style="width: 90%; height: 90%;">
                                </a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-md-6">
            <div class="css-16i2mxe">
                <h2 class="css-kj9vo7">Summary</h2>
                <p>${summary}</p>
                <h2 class="css-kj9vo7">Publications</h2>
                <p>${publications}</p>
            </div>
        </div>
    `;
}

// Data for person 1
const person1Data = {
    name: "Dennis Biström",
    title: "Head of DevLab",
    imagePath: "../../people/Dennis6_BW_cf4910c3e4.webp",
    summary: "Dennis Biström is an IT-Lecturer at Arcada UAS...",
    publications: "Hägglund, S. Tigerstedt, C., Biström, D. Espinosa-Leal, L., ...",
};

// Data for person 2
const person2Data = {
    name: "Kristoffer Kuvaja-Adolfsson",
    title: "Developer",
    imagePath: "../../people/Kristoffer Kuvaja-Adolfsson.webp",
    summary: "Summary of another person...",
    publications: "Publications of another person...",
};

// Generate HTML for person 1
const person1HTML = createPersonCard(person1Data.name, person1Data.title, person1Data.imagePath, person1Data.summary, person1Data.publications);

// Generate HTML for person 2
const person2HTML = createPersonCard(person2Data.name, person2Data.title, person2Data.imagePath, person2Data.summary, person2Data.publications);

// Append the generated HTML to a container element
const container = document.getElementById("people-container");
container.innerHTML = person1HTML + person2HTML; // Add more HTML strings for additional people if needed

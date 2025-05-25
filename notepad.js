document.addEventListener("DOMContentLoaded", loadNotes);

function addNote() {
    let noteText = document.getElementById("note-text").value;
    if (noteText.trim() === "") return;

    let note = {
        id: Date.now(),
        text: noteText,
        timestamp: new Date().toLocaleString()
    };

    let notes = JSON.parse(localStorage.getItem("notes")) || [];
    notes.push(note);
    localStorage.setItem("notes", JSON.stringify(notes));

    document.getElementById("note-text").value = "";
    displayNotes();
}

function displayNotes() {
    let notesContainer = document.getElementById("notes-container");
    notesContainer.innerHTML = "";

    let notes = JSON.parse(localStorage.getItem("notes")) || [];

    notes.forEach(note => {
        let noteDiv = document.createElement("div");
        noteDiv.classList.add("note");
        noteDiv.innerHTML = `
            <p>${note.text}</p>
            <small>${note.timestamp}</small><br>
            <button onclick="deleteNote(${note.id})">Delete</button>
        `;
        notesContainer.appendChild(noteDiv);
    });
}

function deleteNote(id) {
    let notes = JSON.parse(localStorage.getItem("notes")) || [];
    notes = notes.filter(note => note.id !== id);
    localStorage.setItem("notes", JSON.stringify(notes));
    displayNotes();
}

function loadNotes() {
    displayNotes();
}

  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('sw.js')
      .then(reg => console.log('Service Worker registered', reg))
      .catch(err => console.error('Service Worker failed', err));
  }



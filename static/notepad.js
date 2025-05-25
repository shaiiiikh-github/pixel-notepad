document.addEventListener("DOMContentLoaded", loadNotes);

async function loadNotes() {
    try {
        const response = await fetch('/api/notes');
        const notes = await response.json();
        displayNotes(notes);
    } catch (error) {
        console.error("Failed to load notes:", error);
    }
}

async function addNote() {
    const noteText = document.getElementById("note-text").value;
    if (noteText.trim() === "") return;

    try {
        const response = await fetch('/api/notes', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: noteText })
        });

        if (!response.ok) {
            const err = await response.json();
            console.error("Error:", err);
        }

        document.getElementById("note-text").value = "";
        loadNotes();
    } catch (error) {
        console.error("Failed to add note:", error);
    }
}


function displayNotes(notes) {
    const notesContainer = document.getElementById("notes-container");
    notesContainer.innerHTML = "";

    notes.forEach(note => {
        const noteDiv = document.createElement("div");
        noteDiv.classList.add("note");
        noteDiv.innerHTML = `
            <p>${note.text}</p>
            <small>${note.timestamp}</small><br>
            <button onclick="deleteNote(${note.id})">Delete</button>
        `;
        notesContainer.appendChild(noteDiv);
    });
}

async function deleteNote(id) {
    try {
        await fetch(`/api/notes/${id}`, {
            method: 'DELETE'
        });
        loadNotes();
    } catch (error) {
        console.error("Failed to delete note:", error);
    }
}



alert('TA FUNCIONANDO ESSA BAGAÇA');

function lerUsuarios() {
    fetch('/usuarios')
        .then(response => response.json())
        .then(data => {
            const usuariosList = document.getElementById('usuarios-list');
            usuariosList.innerHTML = '';
            data.forEach(usuario => {
                const li = document.createElement('li');
                li.textContent = `Nome: ${usuario.nome}, CPF: ${usuario.cpf}, Data de Nascimento: ${usuario.dataNascimento}`;
                usuariosList.appendChild(li);
            });
        });
}


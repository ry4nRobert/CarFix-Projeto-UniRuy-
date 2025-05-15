var menu = document.querySelectorAll('.item-menu')

function selectIcon(){
    menu.forEach((item)=>
        item.classList.remove('ativo')
    )
    this.classList.add('ativo')
}

menu.forEach((item)=>
    item.addEventListener('click', selectIcon)
)

//Expandir o menu

var btnExp = document.querySelector('#btn-exp')
var menuSide = document.querySelector('.menu-lateral')

btnExp.addEventListener('click', function(){
    menuSide.classList.toggle('expandir')
})

document.addEventListener("DOMContentLoaded", function () {
  const btnAlterarSenha = document.getElementById("btnAlterarSenha");
  const formSenha = document.getElementById("formAlterarSenha");
  const btnConfirmar = document.getElementById("btnConfirmar");

  if (btnAlterarSenha && formSenha && btnConfirmar) {
    btnAlterarSenha.addEventListener("click", function (event) {
      event.preventDefault(); // Impede recarregar
      formSenha.style.display = "block"; // Mostra o formulário
    });

    btnConfirmar.addEventListener("click", function () {
      const novaSenha = document.getElementById("novaSenha").value;
      alert("Nova senha enviada: " + novaSenha);

      // Aqui você pode enviar a nova senha para o backend via fetch/AJAX
    });
  }
});


document.addEventListener("DOMContentLoaded", function () {
    // === ALTERAR SENHA ===
    const btnAlterarSenha = document.getElementById("btnAlterarSenha");
    const liFormSenha = document.getElementById("liFormSenha");
    const btnConfirmar = document.getElementById("btnConfirmar");
    const toggleSenha = document.getElementById("toggleSenha");

    if (btnAlterarSenha && liFormSenha) {
        btnAlterarSenha.addEventListener("click", function (e) {
            e.preventDefault();
            liFormSenha.style.display = liFormSenha.style.display === "none" ? "block" : "none";
        });
    }

    if (btnConfirmar) {
        btnConfirmar.addEventListener("click", function () {
            const senhaAtual = document.getElementById("senhaAtual").value;
            const novaSenha = document.getElementById("novaSenha").value;
            const confirmaSenha = document.getElementById("confirmaSenha").value;

            if (!senhaAtual || !novaSenha || !confirmaSenha) {
                alert("Preencha todos os campos.");
                return;
            }

            if (novaSenha !== confirmaSenha) {
                alert("A nova senha e a confirmação não coincidem.");
                return;
            }

            if (senhaAtual === novaSenha) {
                alert("A nova senha deve ser diferente da atual.");
                return;
            }

            alert("Senha alterada com sucesso!");
            // Aqui você pode enviar os dados ao backend via fetch()
        });
    }

    if (toggleSenha) {
        toggleSenha.addEventListener("click", function () {
            const campos = [
                document.getElementById("senhaAtual"),
                document.getElementById("novaSenha"),
                document.getElementById("confirmaSenha")
            ];

            const novoTipo = campos[0].type === "password" ? "text" : "password";
            campos.forEach(campo => campo.type = novoTipo);
            toggleSenha.textContent = novoTipo === "password" ? "Mostrar" : "Ocultar";
        });
    }

    // ... a parte de e-mail continua igual
});



  const btnAlterarEmail = document.getElementById("btnAlterarEmail"); //FUNÇÃO DA ALTERAÇÃO DE EMAIL
  const liFormEmail = document.getElementById("liFormEmail");
  const btnConfirmarEmail = document.getElementById("btnConfirmarEmail");

  if (btnAlterarEmail && liFormEmail && btnConfirmarEmail) {
    btnAlterarEmail.addEventListener("click", function (event) {
      event.preventDefault();
      liFormEmail.style.display = liFormEmail.style.display === "none" ? "block" : "none";
    });

    btnConfirmarEmail.addEventListener("click", function () {
      const novoEmail = document.getElementById("novoEmail").value;
      const confirmaEmail = document.getElementById("confirmaEmail").value;

      if (!novoEmail || !confirmaEmail) {
        alert("Por favor, preencha ambos os campos de e-mail.");
        return;
      }

      if (novoEmail !== confirmaEmail) {
        alert("Os e-mails não coincidem.");
        return;
      }

      alert("E-mail alterado com sucesso: " + novoEmail);
    
    });
  };

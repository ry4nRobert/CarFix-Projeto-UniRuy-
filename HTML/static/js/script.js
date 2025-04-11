$(document).ready(function(){
    // Scroll para o topo ao clicar no botão
    $(".topo").click(function(){
        $("html, body").animate({ scrollTop: 0 }, 1000);
    });

    // Efeito de opacidade no scroll
    window.addEventListener('scroll', function () {
        var opacity = 1 - Math.min(window.scrollY / 310, 1);
        const formPost = document.querySelector('#formPost');
        const btn_topo = document.querySelector('.topo');

        if (formPost) {
            formPost.style.opacity = opacity.toString();
            if (opacity <= 0) {
                formPost.style.display = 'none';
                formPost.style.height = '10px';
                if (btn_topo) btn_topo.style.display = 'block';
            } else {
                formPost.style.display = 'block';
                formPost.style.height = 'auto';
                if (btn_topo) btn_topo.style.display = 'none';
            }
        }
    });

    // Alternância de seções ao clicar nos botões
    var activeButton = null;
    const buttonConfig = {
        "escolha_formulario_senha": { target: "mudar_senha", resetText: "Mudar senha" },
        "btn_postagens": { target: "postagens", resetText: "Minhas postagens" },
        "btn_mudar_capa": { target: "mudar_capa", resetText: "Mudar foto de capa" },
        "btn_amigos": { target: "amigos", resetText: "Amigos" },
        "btn_mudar_tema": { target: "mudar_tema", resetText: "Mudar Tema" },
        "btn_apagar_conta": { target: "apagar_conta", resetText: "Apagar conta" },
        "btn_mensagens": { target: "mensagens", resetText: "Mensagens" },
        "btn_voltar_config": { target: "feed", text: "Voltar", resetText: "Voltar" },
        "btn_videos": { target: "videos", resetText: "Vídeos" },
        "btn_fotos": { target: "fotos", resetText: "Fotos" }
    };

    $("#escolha_formulario_senha, #btn_postagens, #btn_mudar_capa, #btn_amigos, #btn_mudar_tema, #btn_apagar_conta, #btn_voltar_config, #btn_mensagens, #btn_videos, #btn_fotos").click(function(){
        var clickedId = $(this).attr('id');
        var config = buttonConfig[clickedId];
        if (!config) return;

        if (clickedId === activeButton) {
            $("#" + config.target).hide();
            $("#feed").show();
            $(this).text(config.resetText);
            activeButton = null;
        } else {
            $("#feed, #mudar_senha, #mudar_capa, #amigos, #mudar_tema, #apagar_conta, #mensagens, #postagens, #videos, #fotos").hide();
            $("#" + config.target).show();
            $(this).text("Feed");

            if (activeButton) {
                $("#" + activeButton).text(buttonConfig[activeButton].resetText);
            }

            activeButton = clickedId;
        }
    });

    // Alternância entre menus de configurações
    const btn_config = document.getElementById('btn_config');
    const menu_lateral_esquerdo_1 = document.getElementsByClassName('menu_lateral_esquerdo_1')[0];
    const menu_lateral_esquerdo_2 = document.getElementsByClassName('menu_lateral_esquerdo_2')[0];
    const btn_voltar_config = document.getElementById('btn_voltar_config');

    if (btn_config) {
        btn_config.addEventListener('click', function() {
            if (menu_lateral_esquerdo_1 && menu_lateral_esquerdo_2) {
                menu_lateral_esquerdo_1.style.display = 'none';
                menu_lateral_esquerdo_2.style.display = 'block';
            }
        });
    }

    if (btn_voltar_config) {
        btn_voltar_config.addEventListener('click', function(){
            if (menu_lateral_esquerdo_1 && menu_lateral_esquerdo_2) {
                menu_lateral_esquerdo_1.style.display = 'block';
                menu_lateral_esquerdo_2.style.display = 'none';
            }
        });
    }

    // Modal para troca de foto de perfil
    const fotoPerfil = document.getElementById("foto_perfil");
    if (fotoPerfil) {
        fotoPerfil.addEventListener("click", function() {
            if (document.querySelector(".modal")) return; // Evita múltiplos modais

            if (this.src.includes("user.png")) {
                return;
            }

            if (!confirm("Você tem certeza que deseja mudar sua foto?")) {
                return;
            }

            var modal = document.createElement("div");
            modal.classList.add("modal");
            modal.innerHTML = ` 
                <div class="modal-content">
                    <span class="close">Cancelar</span>
                    <form action="/enviar_foto_perfil" enctype="multipart/form-data" method="post">
                        <input type="file" name="foto" id="foto">
                        <input type="submit" value="Enviar">
                    </form>
                </div>
            `;
            
            document.body.appendChild(modal);

            modal.querySelector(".close").addEventListener("click", function () {
                modal.remove();
            });
        });
    }
});

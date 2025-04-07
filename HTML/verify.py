import random
import smtplib
import email.message

# Gerando um código de 4 dígitos aleatórios
codigo_aleatorio = ''.join(random.choices('0123456789', k=4))
print(f'Código Gerado: {codigo_aleatorio}')

# Função para enviar e-mail
def enviar_email():
    corpo_email = f"""
    <p>Olá,</p>
    <p>Seu código de verificação é: <strong>{codigo_aleatorio}</strong></p>
    <p>Use este código para continuar com seu processo.</p>
    <p>Atenciosamente,</p>
    <p><strong>Seu Nome ou Empresa</strong></p>
    """

    msg = email.message.Message()
    msg['Subject'] = "Seu Código de Verificação"
    msg['From'] = 'seu gmail aqui'  # Remetente
    msg['To'] = 'gmail que vai receber aqui'  # Destinatário
    password = 'SUA_SENHA_DE_APP_AQUI'  # Senha de App do Gmail
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(corpo_email)

    try:
        # Configurando o servidor SMTP do Gmail
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(msg['From'], password)  # Fazendo login com o e-mail e senha de app
        s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
        s.quit()
        print('Email enviado com sucesso!')
    except Exception as e:
        print(f'Erro ao enviar o email: {e}')

# Chamando a função para enviar o e-mail
enviar_email()
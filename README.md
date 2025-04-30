# Integração do FoxESS ao Home Assistant 🏡 ☀

<img src="https://github.com/user-attachments/assets/10df1c52-3325-4f50-98db-debc6b993ec8">

## Instalação
Va até a pasta /homeassistant/custom_components e crie uma pasta chamada foxess_custom

Copie o conteúdo desta pasta de integrações para sua pasta custom_components/foxess_custom

Ficara dessa forma ![image](https://github.com/user-attachments/assets/f9153d00-db9f-4a54-8419-7563530c273f)



## Configuração

Edite seu assistente doméstico /configuration.yaml e adicione:

Link para gerar a token para a API https://www.foxesscloud.com/user/center

     sensor:
       - platform: foxess
         token: seu token gerado pela API
         serial_number: Serial do inversor
         name: "FoxESS"

## Entidades fornecidas

        "Geração do Mês"
        "Geração do Dia"
        "Geração Atual"


![image](https://github.com/user-attachments/assets/7b7bb1b4-6361-483d-b45b-a782bb968761)

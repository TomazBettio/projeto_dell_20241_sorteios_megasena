
function gerarInputs() {
    var divInputs = document.getElementById("inputs_apostas");
    divInputs.innerHTML = ""; 

    for (var i = 1; i <= 5; i++) {
        var label = document.createElement("label");
        label.setAttribute("for", "aposta_usuario" + i);
        label.textContent = "Aposta " + i + ":";
        
        var input = document.createElement("input");
        input.setAttribute("id", "aposta_usuario" + i);
        input.setAttribute("placeholder", "numero");
        input.setAttribute("name", "aposta_usuario" + i);
        input.setAttribute("type", "number");
        input.setAttribute("required", "required");
        
        divInputs.appendChild(label);
        divInputs.appendChild(input);
    }

    document.getElementById("salvarBtn").style.display = "inline-block";
    document.getElementById("gerarBtn").style.display = "none";
}


function submitApostas() {
    var valoresAposta = [];
    for (var i = 1; i <= 5; i++) {
        var valor = document.getElementById("aposta_usuario" + i).value;

        // Verifica se o valor é vazio ou não é um número válido
        if (valor === "" || isNaN(valor)) {
            alert("Por favor, insira um número válido para suas apostas.");
            return false;
        }

        valor = parseInt(valor);

        // Verifica se o valor é zero, se já foi inserido ou se é menor ou igual a 50
        if (valor === 0 || valoresAposta.includes(valor) || valor > 50) {
            alert("Por favor, insira valores únicos, diferentes de zero e maiores que 50 para suas apostas.");
            return false;
        }

        valoresAposta.push(valor);
    }

    document.getElementById("formulario").submit();
}

function funcaoBotao2() {

    var divInputs = document.getElementById("inputs_apostas");
    divInputs.innerHTML = ""; 

    for (var i = 1; i <= 5; i++) {
        var label = document.createElement("label");
        label.setAttribute("for", "aposta_usuario" + i);
        label.textContent = "Aposta " + i + ":";
        
        var input = document.createElement("input");
        input.setAttribute("id", "aposta_usuario" + i);
        input.setAttribute("placeholder", "numero");
        input.setAttribute("name", "aposta_usuario" + i);
        input.setAttribute("type", "number");
        input.setAttribute("required", "required");
        
        divInputs.appendChild(label);
        divInputs.appendChild(input);
    }

    for (var i = 1; i <= 5; i++) {
        var numeros = [];
        for (var i = 1; i <= 5; i++) {
            var numeroAleatorio;
            do {
                numeroAleatorio = Math.floor(Math.random() * 50) + 1;
            } while (numeros.includes(numeroAleatorio) || numeroAleatorio === 0);
            numeros.push(numeroAleatorio);
            document.getElementById("aposta_usuario" + i).value = numeroAleatorio;
    }
    }

    document.getElementById("salvarBtn").style.display = "inline-block";
    document.getElementById("gerarBtn").style.display = "none";
    

}

function formatarCPF(cpf) {
    cpf = cpf.replace(/\D/g, '');

    cpf = cpf.replace(/(\d{3})(\d)/, '$1.$2');
    cpf = cpf.replace(/(\d{3})(\d)/, '$1.$2');
    cpf = cpf.replace(/(\d{3})(\d{1,2})$/, '$1-$2');

    return cpf;
}

function atualizarCPFFormatado() {
    var input = document.getElementById('cpfInput');
    var cpf = input.value;

    if (cpf.length > 14) {
        cpf = cpf.slice(0, 14);
    }

    var cpfFormatado = formatarCPF(cpf);

    input.value = cpfFormatado;
}

document.getElementById('cpfInput').addEventListener('input', atualizarCPFFormatado);
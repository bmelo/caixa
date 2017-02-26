var preloader:MovieClip;
// Nosso MovieClip
var numero:Number = new Number(0);
// Variável numero iniciada com o valor 0
function Init() {
	// Função Init
	_root.stop();
	// Para o filme
	onEnterFrame = function () {
		// Ao entrar no quadro executar a função
		var bl:Number = _root.getBytesLoaded();
		// bl recebe os bytes carregados
		var bt:Number = _root.getBytesTotal();
		// bt recebe os bytes totais
		if (bl>4 && bt>4 && bl>=bt) {
			// Se os bytes carregados forem maior que 4 e os bytes totais forem maior que 4 e bytes carregados forem maior que bytes totais
			delete onEnterFrame;
			// Destrói o evento EnterFrame
			_root.nextFrame();
			// Vá para o próximo quadro
			preloader.unloadMovie();
			// Destrói o MovieClip preloader da memória
		} else {
			// Senão
			numero = Math.floor(bl/bt*100);
			// A variável numero vai receber o arredondamento dos bytes carregados divididos pelos bytes total multiplicados por 100
			preloader.pct = numero+'%';
			// O campo dinâmico vai receber a variável numero mais o caracter %
			preloader.barra._width = numero;
			// O tamanho da barra será o valor da variável número
		}
	};
}
Init();
// Chamamos a função Init

////////////////////////////////////////////////
// Funzioni onLoad
////////////////////////////////////////////////


function caricamento_home(){
    $(function() {
        $("#data").datepicker({ dateFormat: 'dd-mm-yy', minDate: 0/*, maxDate: +30 */});
    });
}

function caricamento_offerta(){
    $("#dataA").datepicker({ dateFormat: 'dd-mm-yy', minDate: 0/*, maxDate: +30 */});
    $("#dataP").datepicker({ dateFormat: 'dd-mm-yy', minDate: 0/*, maxDate: +30 */});
}

function caricamento_messaggi(){
    $('.conversazione').css('cursor','pointer');
    $('.conversazione').click(function(){
        window.location=$(this).find("a").attr("href");
        return false;
    });
}


function caricamento_modifica_profilo(){
    if(Modernizr.csstransforms){
        document.getElementById("chiacchiere0").className = "radioNascosto";
        document.getElementById("chiacchiere1").className = "radioNascosto";
        document.getElementById("chiacchiere2").className = "radioNascosto";
        document.getElementById("chiaImg0").className = "preferenzeImg marginRadioNascosto";
        document.getElementById("chiaImg1").className = "preferenzeImg marginRadioNascosto";
        document.getElementById("chiaImg2").className = "preferenzeImg marginRadioNascosto";

        document.getElementById("musica0").className = "radioNascosto";
        document.getElementById("musica1").className = "radioNascosto";
        document.getElementById("musica2").className = "radioNascosto";
        document.getElementById("musImg0").className = "preferenzeImg marginRadioNascosto";
        document.getElementById("musImg1").className = "preferenzeImg marginRadioNascosto";
        document.getElementById("musImg2").className = "preferenzeImg marginRadioNascosto";

        document.getElementById("animali0").className = "radioNascosto";
        document.getElementById("animali1").className = "radioNascosto";
        document.getElementById("animImg0").className = "preferenzeImg marginRadioNascosto";
        document.getElementById("animImg1").className = "preferenzeImg marginRadioNascosto";

        document.getElementById("fumatori0").className = "radioNascosto";
        document.getElementById("fumatori1").className = "radioNascosto";
        document.getElementById("fumImg0").className = "preferenzeImg marginRadioNascosto";
        document.getElementById("fumImg1").className = "preferenzeImg marginRadioNascosto";
    }
    else{
        console.log("csstransforms not supported");
    }
}

function caricamento_risultati(){
    $('.risultato').css('cursor','pointer');
    $('.risultato').click(function(){
        window.location=$(this).find("a").attr("href");
        return false;
    });
}


function caricamento_notifiche() {
    $('.notifica').css('cursor','pointer');
    $('.notifica').click(function(){
        window.location=$(this).find("a").attr("href");
        return false;
    });
}


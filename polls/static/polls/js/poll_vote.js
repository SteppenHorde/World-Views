// без цикла:
// $( ".voteForm" ).submit(function(event) {
//         // останавливаем обычную отправку с перезагрузкой страницы
//         event.preventDefault();
//
//         // вытаскиваем url
//         var $form = $( this );
//         var url = $form.attr( 'action' );
//
//         // отправка данных
//         var posting = $.post( url, $form.serialize() );
//
//         // действия после получения ответа от сервера
//         posting.done(function( data ) {
//           alert('success');
//         });
//     });


// с циклом
var voteForms = $( ".voteForm" )
// добавляем каждой форме с классом voteForm этот обработчик:
for (var i = 0; i < voteForms.length; i++) {
    // присваиваем обработчик отправки формы
    voteForm = voteForms[i]
    $(voteForm).submit(function(event) {
        // останавливаем обычную отправку с перезагрузкой страницы
        event.preventDefault();

        // вытаскиваем url
        var $form = $( this );
        var url = $form.attr( 'action' );

        // отправка данных
        var posting = $.post( url, $form.serialize() );

        // действия после получения ответа от сервера
        posting.done(function( data ) {
          $form.empty().append(data);
        });
    });
}

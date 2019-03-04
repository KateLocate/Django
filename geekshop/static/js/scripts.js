window.onload = function () {
//    console.log('DOM LOADED');

    $('.basket_list').on('change', 'input[type="number"]', function (event) {
        var target = event.target;
        console.log(target.name, target.value);
        $.ajax({
            //формируем ответ
            url: "/basket/update/" + target.name + "/" + target.value + "/",
            //перегружаем выбранные элементы при получении ответа
            success: function (data) {
                $('.basket_list').html(data.result);
            }
        });
    });
}
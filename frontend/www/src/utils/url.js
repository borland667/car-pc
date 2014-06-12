/*
 * утилиты обработки урлов и т.п.
 */

/**
 * функция дополняет урл GET-параметром
 * @param url - дополняемый урл
 * @param param_name - имя нового параметра
 * @param param_value - значение нового параметра
 * @return - дополненный урл
 */
function addGetParameter(url, param_name, param_value) {
    // проверм есть ли в урле уже GET-параметры
    var have_params = true;
    if (document.URL.indexOf('?') == -1)
        have_params = false;

    if (have_params)
        url += '&';
    else
        url += '?';

    url += param_name +'='+ encodeURIComponent(param_value);
    return url;
}


/**
 * функция для получения GET параметров
 * @param name имя параметра
 * @returns {string}
 */
function getURLParameter(name) {
    return decodeURIComponent(
        (location.search.match(RegExp("[?|&]"+name+'=(.+?)(&|$)'))||[,null])[1]
    );
}

/**
 * функция кодирует переданный словарь данных в строку GET-запроса
 * Пример использования:
 *  var data = { 'first name': 'George', 'last name': 'Jetson', 'age': 110, 'cars': ['lada', 'niva'] };
 *  var querystring = encodeQueryData(data);
 * @param data
 * @returns {string}
 */
function encodeQueryData(data)
{
    var ret = [];
    for (var d in data)
        if (data[d] instanceof Array)
            for (var i=0; i< data[d].length; i++)
                ret.push(encodeURIComponent(d) + "=" + encodeURIComponent(data[d][i]));
        else
            ret.push(encodeURIComponent(d) + "=" + encodeURIComponent(data[d]));
    return ret.join("&");
}
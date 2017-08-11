/**
 * Created by yunpillib on 2017. 6. 4..
 */

var readyToMove = false;

function changeReadyState()
{
    readyToMove = true;
}

function goPrevPage(curr, max) {
    if ( curr == 1 )
        alert("첫 번째 페이지 입니다.");
    else
    {
        var to = curr - 1;

        if ( to < 10 )
            to = '0' + to.toString() + ".html";
        else
            to = to.toString() + ".html";

        location.href = to;
    }
}

function goNextPage(curr, max) {
    if ( curr == max )
        alert("마지막 페이지 입니다.");
    else if ( readyToMove == true || Number(getParam("contentReview")) == 1 )
    {
        var to = curr + 1;

        if ( to < 10 )
            to = '0' + to.toString() + ".html";
        else
            to = to.toString() + ".html";

        location.href = to;
    }
    else if ( readyToMove == false )
    {
        alert("해당 페이지 학습을 완료해야 다음 페이지로 이동이 가능합니다.");
    }
}

function goPage(target) {
    if ( Number(getParam("contentReview")) == 1 )
    {
        var to = target + ".html";
        location.href = to;
    }
    else
    {
        alert("수강을 완료한 후에 페이지 이동이 가능합니다.");
    }
}

$(document).ready(function() {
    $('.menu_btn').mouseover(function () {
        $('.menu1 ul li ul').css('display', 'block');
        $('.menu2 ul li ul').css('display', 'block');
    });

    $('.menu1 ul li ul').mouseleave(function() {
        $('.menu1 ul li ul').css('display', 'none');
    });

    $('.menu2 ul li ul').mouseleave(function() {
        $('.menu2 ul li ul').css('display', 'none');
    });

    $('.f_s_btn a img').click(function () {
        var searchText = 'https://search.naver.com/search.naver?where=nexearch&sm=tab_jum&ie=utf8&query=' + escape($('#search').val());

        window.open(searchText);
    });
});

var getParam = function(key){
        var _parammap = {};
        document.location.search.replace(/\??(?:([^=]+)=([^&]*)&?)/g, function () {
            function decode(s) {
                return decodeURIComponent(s.split("+").join(" "));
            }

            _parammap[decode(arguments[1])] = decode(arguments[2]);
        });

        return _parammap[key];
    };
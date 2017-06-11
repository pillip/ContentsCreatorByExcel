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
    else if ( readyToMove == true )
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
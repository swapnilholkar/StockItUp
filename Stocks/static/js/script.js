function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    crossDomain: false, // obviates need for sameOrigin test
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
        }
    }
});

// function for form submission about stock

function submitStocksForm(stockId) {
    console.log("form submitted currently in ajax script")
    console.log(stockId);

    let questionArray = []
    let answerArray = []
    var alertText="Invalid input for answer, only numbers allowed"

    let validForm = true
    
    $("#stockQuestionForm :input").each(function(){
       
        var question1Id = document.getElementById("5").id;
        var question1Ans = document.getElementById("5").value; 

        var question2Id = document.getElementById("6").id;
        var question2Ans = document.getElementById("6").value;

        var checking_empty = document.forms["questionForm"]["q2Response"].value;
        
        // testing the following for select tag
        console.log(question1Id)
        console.log(question1Ans)
        console.log("for q 2 :")
        console.log(question2Id)
        console.log(question2Ans)
      
        if (question1Id && question2Id) {
            console.log("inside the if statement")
            if (question2Id === "6" && !/^[0-9]*$/.test(question2Ans) || checking_empty=="") {
                console.log("some error")
                // If answer for question 6 is non numeric, this will be run
                validForm = false
                return 
                
            }
            
            console.log(question1Id + " - " + question1Ans + " - " + question2Id  + " - " + question2Ans )
            questionArray.push(question1Id)
            answerArray.push(question1Ans)
            questionArray.push(question2Id)
            answerArray.push(question2Ans)
            
        }
    
        return false;
    });
    
    console.log(`end of loop ${validForm}`)
    if (!validForm) {
        // DO NOTHING
        document.getElementById("alertMessage").innerHTML = alertText;
        // return
    }

    $.ajax({
        type: "POST",
        url:  "/stocksubmission/",
        data: {
            stockId,
            questionArray, //: questionArray.toString(),
            answerArray //: answerArray.toString()
        },
        success: function(result) {
            console.log("response array submitted succesfully");
            console.log(` redirecting to ${result.redirectUrl}`)
            window.location = window.location.origin + "/" + result.redirectUrl
        },
        error: function(error) {
            console.log(error)
            console.log("data submission failed");
        }
      });

}
$(document).ready(function(){

    $("#adCohortBtn").bind('click',function(event)
        { 
            event.preventDefault();
            postStatisticsDatabases("AD Cohort");
            return false;
        });
    $("#obsDataBtn").bind('click',function(event)
        { 
            event.preventDefault();
            postStatisticsDatabases("Observational Data Sources");
            return false;
        });
});

//when you invocke the "statistics" button
function postStatisticsDatabases(type){
    $('#compare_form').attr('action', 'statistics/example');
    console.log("sim");
    postComparisonStatistics(type);
    return true; 
};

//identify type of database
function postComparisonStatistics(type){
  if(a != undefined && a.plugin != undefined){
      $('#comparedbs').html('');
      $('#comparedbs').append('<input type="checkbox" name="chks_'+type+'" checked>');
      $('#submitdbsimulate').click();
  }

}
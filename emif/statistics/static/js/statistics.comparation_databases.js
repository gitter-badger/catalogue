$(document).ready(function(){

    $("#statistics").bind('click',function(event)
        { 
          console.log("OLA");
          event.preventDefault();

          postStatisticsDatabases();
          return false;
        });

});

//when you invocke the "statistics" button
function postStatisticsDatabases(){
    $('#compare_form').attr('action', 'statistics/dbStatistics');
    console.log("sim");
    postComparisonStatistics(false);

   return true; 
};

//load the checkboxs selected
function postComparisonStatistics(isdbs){
  //$('#result_form').submit();
  //console.log('A: '+a);
  //console.log('A-plugin: '+a.plugin);
  if(a != undefined && a.plugin != undefined){
    $('#comparedbs').html('');

    var dbs = a.plugin.getExtraObjects().selectedList;
    //console.error(dbs.length);

    for(var i=0;i<dbs.length;i++){
      $('#comparedbs').append('<input type="checkbox" name="chks_'+dbs[i]+'" checked>');
    }
    var ids = []; 
    $('[name^="chks_"]').each(function(){

      var id = $(this).attr('name').split('_')[1];
      ids.push(id);
      
    });
    $('#submitdbsimulate').click();
  }

}
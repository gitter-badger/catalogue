$(function(){
    var columns = [
                    { "data": "logo", "orderable": false, "searchable": false,
                        "createdCell": function (td, cellData, rowData, row, col) {
                            $(td).html('<center><img style="height: 32px" src="'+cellData+'" /></center>');
                        }
                    },
                    { "data": "name" },
                    { "data": "date_created" },
                    { "data": "members"},
                    { "data": "manage", "orderable": false, "searchable": false,
                        "createdCell": function (td, cellData, rowData, row, col) {
                            switch(cellData){
                                case 'admin':

                                    $(td).html('<img style="height: 32px;" src="https://cdn2.iconfinder.com/data/icons/picons-essentials/71/settings_2-512.png" />');
                                    break;

                                case 'requester':
                                    $(td).html('<img style="height: 32px;" src="https://cdn2.iconfinder.com/data/icons/windows-8-metro-style/512/add_user.png" />');
                                break;
                                case 'member':
                                    $(td).html('<img style="height: 32px;" src="https://cdn4.iconfinder.com/data/icons/eldorado-user/40/registered_user-512.png" />');

                                break;
                                case 'blocked':

                                    $(td).html('<img style="height: 32px;" src="http://uxrepo.com/static/icon-sets/iconic/svg/block.svg" />');
                                break;
                                default:
                                    $(td).html('ERROR');

                            }
                        }
                    }
                ];

    var table = $('#results-table').DataTable( {
        "orderCellsTop": true,
        "paging": true,
        "processing": true,
        "serverSide": true,
        "order": [[1, "asc"]],
        "sDom": '<"table_top" ir>t<"table_footer" lJp><"clear">',
        "ajax": {
            "url": "communities/list/filters",
            "type": "POST"
        },
        "columns": columns

    } );

    table.columns().eq( 0 ).each( function ( colIdx ) {

        $('.finput'+colIdx).on( 'keyup change', function () {
            table
                .column( colIdx )
                .search( this.value )
                .draw();
        } );
    } );

    $('#results-table_processing').addClass('alert');
    $('#results-table_processing').addClass('alert-info');
});

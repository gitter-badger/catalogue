$(function(){
    var columns = [
                    { "data": "logo", "orderable": false, "searchable": false,
                        "createdCell": function (td, cellData, rowData, row, col) {
                            $(td).html('<img style="height: 32px" src="'+cellData+'" />');
                        }
                    },
                    { "data": "name" },
                    { "data": "date_created" },
                    { "data": "members"},
                    { "data": "manage", "orderable": false, "searchable": false,
                        "createdCell": function (td, cellData, rowData, row, col) {
                            if(cellData == false)
                                $(td).html('<button class="btn btn-info">Request membership</button>');
                            else
                                $(td).html('Already a member');
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

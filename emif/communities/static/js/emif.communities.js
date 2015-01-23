/*
    # -*- coding: utf-8 -*-
    # Copyright (C) 2014 Ricardo F. Gonçalves Ribeiro and Universidade de Aveiro
    #
    # Authors: Ricardo F. Gonçalves Ribeiro <ribeiro.r@ua.pt>
    #
    # This program is free software: you can redistribute it and/or modify
    # it under the terms of the GNU General Public License as published by
    # the Free Software Foundation, either version 3 of the License, or
    # (at your option) any later version.
    #
    # This program is distributed in the hope that it will be useful,
    # but WITHOUT ANY WARRANTY; without even the implied warranty of
    # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    # GNU General Public License for more details.
    #
    # You should have received a copy of the GNU General Public License
    # along with this program.  If not, see <http://www.gnu.org/licenses/>.
    #
*/
var dashzone;
$(function(){
    dashzone = $("#communitydash").dashboard(
        {
            showRegistry: true,
            registryTarget: "#dashboardselectbox",
            initial: function () {
                dashzone.addWidget("helper");
                dashzone.addWidget("mycommunities");
                dashzone.addWidget("news");
                dashzone.addWidget("fastlinks");

            }
        });


    // Registering plugins on dashboard
    dashzone.register(new HelperWidget("helper", 4, 1, 1, 1));
    dashzone.register(new MyCommunitiesWidget("mycommunities", 2, 2, 5, 1));
    dashzone.register(new NewsWidget("news", 4, 2, 1, 2));
    dashzone.register(new FastLinksWidget("fastlinks", 2, 1, 5, 3));


    var any_configuration = dashzone.loadConfiguration();

    if(any_configuration == false){
        dashzone.initial();
    }

    $('#dashboardreset').tooltip({
        'container': 'body'
    });
});


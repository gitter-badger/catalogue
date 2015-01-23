/*
    # -*- coding: utf-8 -*-
    # Copyright (C) 2015 Ricardo F. Gonçalves Ribeiro and Universidade de Aveiro
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
var MyCommunitiesWidget = function MyCommunitiesWidget(widgetname, width, height, pos_x, pos_y){

    MyCommunitiesWidget._base.apply(this, [widgetname, "My Communities", width, height, pos_x, pos_y]);

}.inherit(DashboardWidget).addToPrototype({
    __init : function(gridster, parent){
        var self = this;

        self.icon = '';

        self.content = '<table style="margin-bottom:0px;" class="table table-striped">\
            <tr><td><img width="70px" src="http://127.0.0.1:8000/static/img/emif_logo_trans.png" /></td><td class="list_middle lead">EMIF Catalogue</td></tr>\
            <tr><td><img width="70px" src="http://i.vimeocdn.com/portrait/8815135_300x300.jpg" /></td><td class="list_middle">UK-DP</td></tr>\
            <tr><td><img width="70px" src="https://cdn0.iconfinder.com/data/icons/chart-graphics/78/Diagram_and_infographic_icons-03-512.png" /></td><td class="list_middle">Community 1</td></tr>\
            <tr><td><img width="70px" src="https://cdn0.iconfinder.com/data/icons/chart-graphics/78/Diagram_and_infographic_icons-03-512.png" /></td><td class="list_middle">Community with big name 2</td></tr>\
        </table>\
        <ul style="margin:0px;" class="pager">\
            <li><a href="#">Previous</a></li>\
            <li><a href="#">Next</a></li>\
        </ul>\
        ';

        MyCommunitiesWidget._super.__init.apply(self, [gridster, parent]);

        $('.table', $('#'+self.widgetname)).parent().css('padding', '0px');

    }
});

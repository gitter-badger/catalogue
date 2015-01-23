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
var HelperWidget = function HelperWidget(widgetname, width, height, pos_x, pos_y){

    HelperWidget._base.apply(this, [widgetname, "The Basics", width, height, pos_x, pos_y]);

}.inherit(DashboardWidget).addToPrototype({
    __init : function(gridster, parent){
        var self = this;

        self.icon = '';


        var bl = $('#base_link').attr('href');

        self.content = '\
                <div class="helper-container">\
                <a class="helperthumb thumbnail">\
                  <img data-src="holder.js/300x200" alt="300x200"\
                  src="'+bl+'static/img/learn.png">\
                </a>\
                 <a class="helperthumb thumbnail">\
                  <img data-src="holder.js/300x200" alt="300x200"\
                  src="'+bl+'static/img/create_communities.png">\
                </a>\
                 <a class="helperthumb thumbnail">\
                  <img data-src="holder.js/300x200" alt="300x200"\
                  src="'+bl+'static/img/invite.png">\
                </a>\
                 <a class="helperthumb thumbnail">\
                  <img data-src="holder.js/300x200" alt="300x200"\
                  src="'+bl+'static/img/share.png">\
                </a>\
                </div>\
        ';

        //"<center><h3>Loading...</h3></center>";

        HelperWidget._super.__init.apply(self, [gridster, parent]);

    }
});

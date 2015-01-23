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
var NewsWidget = function NewsWidget(widgetname, width, height, pos_x, pos_y){

    NewsWidget._base.apply(this, [widgetname, "Recent News", width, height, pos_x, pos_y]);

}.inherit(DashboardWidget).addToPrototype({
    __init : function(gridster, parent){
        var self = this;

        self.icon = '';

        self.content = '\
            <div class="news-container">';

        var news = '    <div class="new">\
                    <div class="newscolmask leftmenu">\
                        <div class="newscolright">\
                            <div class="tcontainer-colwrap">\
                                <div class="new-tcontainer">\
                                        <div class="new-title"><h4>New features for communities</h4></div>\
                                            <small><div class="pull-left new-poster">Posted by: Administrator of Catalogue</div>\
                                        <div class="pull-right new-comments"><i class="fa fa-comments"></i> 24</div></small>\
                                    </div>\
                            </div>\
                            <div class="new-date-col">\
                                <div class="thumbnail new-date">\
                                    <div><div class="new-pill">23<br />Jan</div></div>\
                                </div>\
                            </div>\
                        </div>\
                    </div>\
                    <div class="new-body">\
                    <img class="newsthumb thumbnail" src="http://banda.ie/wp-content/uploads/Business.jpg" />\
                    <p>\
                        On the other hand, we denounce with righteous indignation and dislike men who are so beguiled and demoralized by the charms of pleasure of the moment, so blinded by desire, that they cannot foresee the pain and trouble that are bound to ensue; and equal blame belongs to those who fail in their duty through weakness of will, which is the same as saying through shrinking from toil and pain.\
                        </p>\
                        <p>These cases are perfectly simple and easy to distinguish. In a free hour, when our power of choice is untrammelled and  when our power of choice is untrammelled and when nothing prevents our being able to do what we like best, every pleasure is to be welcomed and every pain avoided. \
                    </p>\
                    </div>\
                    <div class="clearfix new-footer">\
                        <button class="pull-right btn">Read more</button>\
                    </div>\
                    <hr />\
                </div>';
        self.content+= news + news + news;
        self.content+=    '</div>';

        //"<center><h3>Loading...</h3></center>";

        NewsWidget._super.__init.apply(self, [gridster, parent]);

    }
});

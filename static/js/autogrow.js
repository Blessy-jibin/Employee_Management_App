angular.module("workToJob").directive("autoGrow", function(){
    return function(scope, element, attr){
        var update = function(){
            element.css("height", "auto");
            var height = element[0].scrollHeight;
            if(height > 0){
                element.css("height", height + "px");
            }
        };
        scope.$watch(attr.ngModel, function(){
            update();
        });
        attr.$set("ngTrim", "false");
    };
});
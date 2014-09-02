<html>

    <head>
        <link href="/static/css/bootstrap.min.css" rel="stylesheet">
    </head>

    <body>
        <div class="container-fluid">
            <div class="row">
                <div class="col-md-12" style="background-color:#333333">
                    <h1 style="color:white; margin: 8px">Zenoss Inspector</h1>
                </div>
            </div>
            <div class="row">
                <div class="col-md-2" style="margin-top:20px; height: 100%">
                    <ul class="list-unstyled">
                        % for row in rows:
                            <li><span class="btn btn-link" onclick="showpanel('{{row[0]}}-panel')">{{row[0]}}</span></li>
                        % end
                    </ul>
                </div>
                <div class="col-md-10">
                    % for row in rows:
                        <div id="{{row[0]}}-panel">
                            <h2>{{row[0]}}</h2>
                            <ul class="nav nav-tabs" role="tablist">
                                <li class="active"><a href="#{{row[0]}}-stdout" role="tab" data-toggle="tab">stdout</a></li>
                                <li><a href="#{{row[0]}}-stderr" role="tab" data-toggle="tab">stderr</a></li>
                            </ul>
                            <div class="tab-content">
                                <div class="tab-pane active" id="{{row[0]}}-stdout">
                                    <pre style="border: none; border-radius: 0px">{{row[2]}}</pre>
                                </div>
                                <div class="tab-pane" id="{{row[0]}}-stderr">
                                    <pre style="border: none; border-radius: 0px">{{row[3]}}</pre>
                                </div>
                            </div>
                        </div>
                    %end
                </div>
            </div>
        </div>
    <body>
    <script src="/static/js/jquery.min.js"></script>
    <script src="/static/js/jquery.timeago.js"></script>
    <script src="/static/js/bootstrap.min.js"></script>
    <script>
        $("abbr.timeago").timeago();

        function showpanel(id) {
            $("[id$=-panel]").each(function(i, item) {
                if (item.id === id) {
                    $(item).show();
                } else {
                    $(item).hide();
                }
            });
        }

        showpanel("{{rows[0][0]}}-panel");
    </script>
</html>
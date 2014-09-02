<html>

    <head>
        <script src="/static/js/jquery.min.js"></script>
        <script src="/static/js/jquery.timeago.js"></script>
        <script src="/static/js/bootstrap.min.js"></script>
        <link href="/static/css/bootstrap.min.css" rel="stylesheet">
    </head>

    <body>
        <div class="container-fluid">
            <div class="row">
                <div class="col-md-12" style="background-color:#333333; padding: 8px">
                    <a href="/">
                        <img height="39" src="/static/img/zenoss_logo_trans.png">
                    </a>
                </div>
            </div>
        </div>
        <div class="container">
            <h2>Recent Inspections</h2>
            <table class="table table-striped">
                <tr>
                    <th>Inspection ID</th>
                    <th>Hostname</th>
                    <th>Time</th>
                </tr>
                % for row in rows:
                    <tr>
                        <td style="font-family: monospace"><a href="/inspection/{{row[0]}}">{{row[0]}}</a></td>
                        <td>{{row[1]}}</td>
                        <td><abbr class="timeago" title="{{row[2]}}">{{row[2]}}</abbr></td>
                    </tr>
                % end
            </table>
        </div>
    <body>
    <script>
        $("abbr.timeago").timeago();
    </script>

</html>
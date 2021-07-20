# Copyright 2012-2014 VPAC
#
# This file is part of pytsm.
#
# pytsm is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pytsm is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pytsm.  If not, see <http://www.gnu.org/licenses/>.

from ..base import TsmCommand


class Command(TsmCommand):
    help = "List number of archives objects and size by management class for a specific node"

    def handle_tsm(self, args, f, d):
        f.output_head("Archive Objects")

        results = d.execute("""SELECT a.node_name, a.class_name, CAST(FLOAT(SUM(ao.bfsize))/1024/1024/1024 as DEC(14,1)) as size_gb, count(ao.bfsize) as number_of_objects
               FROM  archives a, archive_objects ao
               WHERE a.object_id=ao.objid and a.node_name='DEHZE01-LSV001'
               GROUP BY a.node_name, a.class_name
""")

        headers = [
            {"name": "Node Name",},
            {"name": "Class Name", },
            {"name": "Size [GB]", "justify": "right",
                "format": "float", "spec": "%0.1f"},
            {"name": "Number Of Objects", "justify": "right",
                "format": "integer", "spec": "%0.0f"},
        ]
        f.output_results(results, headers)

        d.close()

        f.output_tail()

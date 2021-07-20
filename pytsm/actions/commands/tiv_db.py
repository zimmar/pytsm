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
    help = "Selecting specific columns from db table"

    def handle_tsm(self, args, f, d):
        f.output_head("DB Table")

        results = d.execute(
            """SELECT 
            tot_file_system_mb, 
            used_db_space_mb, 
            free_space_mb,
            (SELECT CAST(SUM(100-(free_space_mb*100) / tot_file_system_mb) AS DECIMAL(3,1)) AS PCT_UTILIZED 
            FROM db), last_backup_date FROM db"""
        )

        headers = [
            {"name": "Total Files System [mb]", "justify": "right",
                "format": "integer", "spec": "%0.0f"},
            {"name": "Used Db Space [mb]", "justify": "right",
                "format": "integer", "spec": "%0.0f"},
            {"name": "Free Space [mb]", "justify": "right",
                "format": "integer", "spec": "%0.0f"},
            {"name": "PCT Utilized", "justify": "right",
                "format": "float", "spec": "%3.1f"},
            {"name": "Last Backup"}
        ]
        f.output_results(results, headers)

        d.close()

        f.output_tail()

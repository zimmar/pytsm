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
    help = "Management classes with archive copy group information"

    def handle_tsm(self, args, f, d):
        f.output_head("Archive Management Classes")

        results = d.execute("""SELECT
    mgmtclasses.domain_name, mgmtclasses.set_name, mgmtclasses.class_name, mgmtclasses.defaultmc,
    ar_copygroups.retver, ar_copygroups.destination
FROM
    mgmtclasses mgmtclasses, ar_copygroups ar_copygroups
WHERE
    mgmtclasses.domain_name = ar_copygroups.domain_name AND
    mgmtclasses.set_name = ar_copygroups.set_name AND
    mgmtclasses.class_name = ar_copygroups.class_name AND
    mgmtclasses.set_name='ACTIVE'
ORDER BY
    mgmtclasses.domain_name, mgmtclasses.set_name, mgmtclasses.class_name
""")

        headers = [
            {"name": "Domain Name",},
            {"name": "Policy Set Name", },
            {"name": "Class Name", },
            {"name": "Default MC", },
            {"name": "Retantion", },
            {"name": "Destination", },
        ]
        f.output_results(results, headers)

        d.close()

        f.output_tail()

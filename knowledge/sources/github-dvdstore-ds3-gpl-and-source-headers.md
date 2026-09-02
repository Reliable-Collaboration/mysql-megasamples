---
type: Source
title: ds3/gpl.txt and the GPL headers in the DS3 generator/driver sources
description: The kit ships GPL version 2 (June 1991) text; C generators and C# driver sources declare "GNU General Public License ... either version 2 of the License, or (at your option) any later version" with Dell (2005) / VMware (2014) copyright.
resource: https://raw.githubusercontent.com/dvdstore/ds3/master/ds3/gpl.txt
tags: [dvdstore, ds3, license, gpl-2-0]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://raw.githubusercontent.com/dvdstore/ds3/master/ds3/gpl.txt
    title: gpl.txt (18,013 bytes; md5 ebf4e8b49780ab187d51bd26aaa022c6)
    accessed: 2026-09-02
  - resource: https://raw.githubusercontent.com/dvdstore/ds3/master/ds3/data_files/cust/ds3_create_cust.c
    title: ds3_create_cust.c header
    accessed: 2026-09-02
  - resource: https://raw.githubusercontent.com/dvdstore/ds3/master/ds3/data_files/reviews/ds3_create_reviews.c
    title: ds3_create_reviews.c header
    accessed: 2026-09-02
  - resource: https://raw.githubusercontent.com/dvdstore/ds3/master/ds3/data_files/membership/ds3_create_membership.c
    title: ds3_create_membership.c header
    accessed: 2026-09-02
  - resource: https://raw.githubusercontent.com/dvdstore/ds3/master/ds3/mysqlds3/ds3mysqlfns.cs
    title: ds3mysqlfns.cs header
    accessed: 2026-09-02
---

# What was read
gpl.txt in full (also copied at ds3/mysqlds3/gpl.txt and ds3/oracleds3/gpl.txt) and the first 25 lines of the listed sources, accessed 2026-09-02.

# Relevant excerpt
* gpl.txt: "GNU GENERAL PUBLIC LICENSE Version 2, June 1991 Copyright (C) 1989, 1991 Free Software Foundation, Inc." Section 2(b): "You must cause any work that you distribute or publish, that in whole or in part contains or is derived from the Program or any part thereof, to be licensed as a whole at no charge to all third parties under the terms of this License." Section 2 also: "In addition, mere aggregation of another work not based on the Program with the Program (or with a work based on the Program) on a volume of a storage or distribution medium does not bring the other work under the scope of this License." Section 0: "The act of running the Program is not restricted, and the output from the Program is covered only if its contents constitute a work based on the Program (independent of having been made by running the Program)."
* ds3_create_cust.c / ds3_create_reviews.c: "Copyright (C) 2005 Dell, Inc. <dave_jaffe@dell.com> and <tmuirhead@vmware.com> ... This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version." ds3_create_membership.c: "Copyright (C) 2014 VMware, Inc.". ds3mysqlfns.cs: same GPL v2-or-later header, Dell 2005.
* The SQL build scripts (mysqlds3_create_db.sql etc.) carry no license header of their own; they are distributed inside the same GPL kit.

# What it was used to decide
[GPL-2.0 license record](/licenses/gpl-2-0.md); [generated-data license question](/questions/dvdstore-generated-data-license.md).

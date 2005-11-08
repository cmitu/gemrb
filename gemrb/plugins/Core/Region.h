/* GemRB - Infinity Engine Emulator
 * Copyright (C) 2003 The GemRB Project
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * as published by the Free Software Foundation; either version 2
 * of the License, or (at your option) any later version.

 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.

 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
 *
 * $Header: /data/gemrb/cvs2svn/gemrb/gemrb/gemrb/plugins/Core/Region.h,v 1.12 2005/11/08 22:59:05 edheldil Exp $
 *
 */

/**
 * @file Region.h
 * Declares Point and Region, 2d-space primitive types
 * @author The GemRB Project
 */


#ifndef REGION_H
#define REGION_H

#ifdef WIN32

#ifdef GEM_BUILD_DLL
#define GEM_EXPORT __declspec(dllexport)
#else
#define GEM_EXPORT __declspec(dllimport)
#endif

#else
#define GEM_EXPORT
#endif

/**
 * @class Point
 * Point in 2d-space: [x, y]
 */

class GEM_EXPORT Point {
public:
	Point(void);
	~Point(void);
	short x,y;
	Point(const Point& pnt);
	Point& operator=(const Point& pnt);
	bool operator==(const Point &pnt);
	bool operator!=(const Point &pnt);
	Point(short x, short y);
	/** if it is [-1.-1] */
	bool isempty() const;
};


/**
 * @class Region
 * Rectangular area in 2d-space [x, y] - [x+w, y+h]
 */

class GEM_EXPORT Region {
public:
	Region(void);
	~Region(void);
	int x;
	int y;
	int w;
	int h;
	Region(const Region& rgn);
	Region(const Point& p, int w, int h);
	Region& operator=(const Region& rgn);
	bool operator==(const Region& rgn);
	bool operator!=(const Region& rgn);
	Region(int x, int y, int w, int h);
	bool PointInside(unsigned short XPos, unsigned short YPos);
	bool PointInside(Point &p);
	bool InsideRegion(Region& rgn);
	void Normalize();
};

#endif  // ! REGION_H

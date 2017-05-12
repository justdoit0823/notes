
PostgreSQL Timestamp
====================

PostgreSQL中timestamp存在两种形式，timestamp with time zone(timestamp) 和 timestamp without time zone(timestamptz)。
相比于timestamp, 本质上没大多差别，都是相比一个特定时间点的偏移，只是描述timestamptz时会加上特定的时区信息。

使用
====

  * 应用程序

存储datetime时，可以根据是否需要时区信息来选择timestamp或者timestamptz。例如，在Django的orm中两种类型对应的都是DateTimeField，但是可以配置时区信息。

  * 时间解析

在解析时间时，timestamp会忽略当前session的时区信息，而按照UTC；相反，timestamptz会根据当前session的时区信息来处理。


```
workspace=# select extract(epoch from '2016-11-03 17:40:00'::timestamptz);
 date_part
------------
 1478166000
(1 row)

workspace=# select extract(epoch from '2016-11-03 17:40:00'::timestamp);
 date_part
------------
 1478194800
(1 row)

workspace=# show timezone;
 TimeZone
----------
 PRC
(1 row)
```


Timestamp实现
=============

内部数据结构
------------

  * Timestamp/TimestampTz


定义在src/include/datatype/timestamp.h中42行处，具体如下：

		#ifdef HAVE_INT64_TIMESTAMP

		typedef int64 Timestamp;
		typedef int64 TimestampTz;
		typedef int64 TimeOffset;
		typedef int32 fsec_t;			/* fractional seconds (in microseconds) */
		#else

		typedef double Timestamp;
		typedef double TimestampTz;
		typedef double TimeOffset;
		typedef double fsec_t;			/* fractional seconds (in seconds) */
		#endif


  * pg_tm

定义在src/include/pgtime.h中25行处，具体如下：

```
struct pg_tm
{
	int			tm_sec;
	int			tm_min;
	int			tm_hour;
	int			tm_mday;
	int			tm_mon;			/* origin 0, not 1 */
	int			tm_year;		/* relative to 1900 */
	int			tm_wday;
	int			tm_yday;
	int			tm_isdst;
	long int	tm_gmtoff;
	const char *tm_zone;
};
```

  * 存储内容


Julian-date格式存储，内容为相对于2000年1月1日偏移的秒数，也就是存在正负。相关宏定义在src/include/datatype/timestamp.h中169行处，具体如下：

	/* Julian-date equivalents of Day 0 in Unix and Postgres reckoning */
	#define UNIX_EPOCH_JDATE		2440588 /* == date2j(1970, 1, 1) */
	#define POSTGRES_EPOCH_JDATE	2451545 /* == date2j(2000, 1, 1) */


routine实现
-----------

		
主要包含timestamp\_in和timestamp\_out(处理Timestamp), timestamptz\_in和timestamptz_out(处理TimestampTz), timestamp2tm, tm2timestamp, EncodeDateTime, DecodeDateTime8个。

  * timestamp_in

函数功能是把日期字符串转换成内部Timestamp，定义在src/backend/utils/adt/timestamp.c中136行处，具体如下：


```
Datum
timestamp\_in(PG_FUNCTION_ARGS)
{
	char	   *str = PG_GETARG_CSTRING(0);

#ifdef NOT_USED
	Oid			typelem = PG_GETARG_OID(1);
#endif
	int32		typmod = PG_GETARG_INT32(2);
	Timestamp	result;
	fsec_t		fsec;
	struct pg_tm tt,
			   *tm = &tt;
	int			tz;
	int			dtype;
	int			nf;
	int			dterr;
	char	   *field[MAXDATEFIELDS];
	int			ftype[MAXDATEFIELDS];
	char		workbuf[MAXDATELEN + MAXDATEFIELDS];

	dterr = ParseDateTime(str, workbuf, sizeof(workbuf),
						  field, ftype, MAXDATEFIELDS, &nf);
	if (dterr == 0)
		dterr = DecodeDateTime(field, ftype, nf, &dtype, tm, &fsec, &tz);
	if (dterr != 0)
		DateTimeParseError(dterr, str, "timestamp");

	switch (dtype)
	{
		case DTK_DATE:
			if (tm2timestamp(tm, fsec, NULL, &result) != 0)
				ereport(ERROR,
						(errcode(ERRCODE_DATETIME_VALUE_OUT_OF_RANGE),
						 errmsg("timestamp out of range: \"%s\"", str)));
			break;

		case DTK_EPOCH:
			result = SetEpochTimestamp();
			break;

		case DTK_LATE:
			TIMESTAMP_NOEND(result);
			break;

		case DTK_EARLY:
			TIMESTAMP_NOBEGIN(result);
			break;

		case DTK_INVALID:
			ereport(ERROR,
					(errcode(ERRCODE_FEATURE_NOT_SUPPORTED),
			  errmsg("date/time value \"%s\" is no longer supported", str)));

			TIMESTAMP_NOEND(result);
			break;

		default:
			elog(ERROR, "unexpected dtype %d while parsing timestamp \"%s\"",
				 dtype, str);
			TIMESTAMP_NOEND(result);
	}

	AdjustTimestampForTypmod(&result, typmod);

	PG_RETURN_TIMESTAMP(result);
}

```


  * timestamp_out

函数功能是把内部Timestamp转换成日期字符串，定义在src/backend/utils/adt/timestamp.c中207行处，具体如下：

```
Datum
timestamp_out(PG_FUNCTION_ARGS)
{
	Timestamp	timestamp = PG_GETARG_TIMESTAMP(0);
	char	   *result;
	struct pg_tm tt,
			   *tm = &tt;
	fsec_t		fsec;
	char		buf[MAXDATELEN + 1];

	if (TIMESTAMP_NOT_FINITE(timestamp))
		EncodeSpecialTimestamp(timestamp, buf);
	else if (timestamp2tm(timestamp, NULL, tm, &fsec, NULL, NULL) == 0)
		EncodeDateTime(tm, fsec, false, 0, NULL, DateStyle, buf);
	else
		ereport(ERROR,
				(errcode(ERRCODE_DATETIME_VALUE_OUT_OF_RANGE),
				 errmsg("timestamp out of range")));

	result = pstrdup(buf);
	PG_RETURN_CSTRING(result);
}

```

  * timestamptz_in

函数功能是把日期字符串转换成内部TimestampTz，定义在src/backend/utils/adt/timestamp.c中410行处，具体如下：

```
Datum
timestamptz_in(PG_FUNCTION_ARGS)
{
	char	   *str = PG_GETARG_CSTRING(0);

#ifdef NOT_USED
	Oid			typelem = PG_GETARG_OID(1);
#endif
	int32		typmod = PG_GETARG_INT32(2);
	TimestampTz result;
	fsec_t		fsec;
	struct pg_tm tt,
			   *tm = &tt;
	int			tz;
	int			dtype;
	int			nf;
	int			dterr;
	char	   *field[MAXDATEFIELDS];
	int			ftype[MAXDATEFIELDS];
	char		workbuf[MAXDATELEN + MAXDATEFIELDS];

	dterr = ParseDateTime(str, workbuf, sizeof(workbuf),
						  field, ftype, MAXDATEFIELDS, &nf);
	if (dterr == 0)
		dterr = DecodeDateTime(field, ftype, nf, &dtype, tm, &fsec, &tz);
	if (dterr != 0)
		DateTimeParseError(dterr, str, "timestamp with time zone");

	switch (dtype)
	{
		case DTK_DATE:
			if (tm2timestamp(tm, fsec, &tz, &result) != 0)
				ereport(ERROR,
						(errcode(ERRCODE_DATETIME_VALUE_OUT_OF_RANGE),
						 errmsg("timestamp out of range: \"%s\"", str)));
			break;

		case DTK_EPOCH:
			result = SetEpochTimestamp();
			break;

		case DTK_LATE:
			TIMESTAMP_NOEND(result);
			break;

		case DTK_EARLY:
			TIMESTAMP_NOBEGIN(result);
			break;

		case DTK_INVALID:
			ereport(ERROR,
					(errcode(ERRCODE_FEATURE_NOT_SUPPORTED),
			  errmsg("date/time value \"%s\" is no longer supported", str)));

			TIMESTAMP_NOEND(result);
			break;

		default:
			elog(ERROR, "unexpected dtype %d while parsing timestamptz \"%s\"",
				 dtype, str);
			TIMESTAMP_NOEND(result);
	}

	AdjustTimestampForTypmod(&result, typmod);

	PG_RETURN_TIMESTAMPTZ(result);
}
```

  * timestamptz_out

函数功能是把内部TimestampTz转换成日期字符串，定义在src/backend/utils/adt/timestamp.c中726行处，具体如下：

```
Datum
timestamptz_out(PG_FUNCTION_ARGS)
{
	TimestampTz dt = PG_GETARG_TIMESTAMPTZ(0);
	char	   *result;
	int			tz;
	struct pg_tm tt,
			   *tm = &tt;
	fsec_t		fsec;
	const char *tzn;
	char		buf[MAXDATELEN + 1];

	if (TIMESTAMP_NOT_FINITE(dt))
		EncodeSpecialTimestamp(dt, buf);
	else if (timestamp2tm(dt, &tz, tm, &fsec, &tzn, NULL) == 0)
		EncodeDateTime(tm, fsec, true, tz, tzn, DateStyle, buf);
	else
		ereport(ERROR,
				(errcode(ERRCODE_DATETIME_VALUE_OUT_OF_RANGE),
				 errmsg("timestamp out of range")));

	result = pstrdup(buf);
	PG_RETURN_CSTRING(result);
}
```

  * timestamp2tm

函数功能主要是把Timestamp或者TimestampTz转换成POSIX time结构(pg_tm)，定义在src/backend/utils/adt/timestamp.c中1784行处，具体如下：

```
int
timestamp2tm(Timestamp dt, int *tzp, struct pg_tm * tm, fsec_t *fsec, const char **tzn, pg_tz *attimezone)
{
	Timestamp	date;
	Timestamp	time;
	pg_time_t	utime;

	/* Use session timezone if caller asks for default */
	if (attimezone == NULL)
		attimezone = session_timezone;

#ifdef HAVE_INT64_TIMESTAMP
	time = dt;
	TMODULO(time, date, USECS_PER_DAY);

	if (time < INT64CONST(0))
	{
		time += USECS_PER_DAY;
		date -= 1;
	}

	/* add offset to go from J2000 back to standard Julian date */
	date += POSTGRES_EPOCH_JDATE;

	/* Julian day routine does not work for negative Julian days */
	if (date < 0 || date > (Timestamp) INT_MAX)
		return -1;

	j2date((int) date, &tm->tm_year, &tm->tm_mon, &tm->tm_mday);
	dt2time(time, &tm->tm_hour, &tm->tm_min, &tm->tm_sec, fsec);
#else
	time = dt;
	TMODULO(time, date, (double) SECS_PER_DAY);

	if (time < 0)
	{
		time += SECS_PER_DAY;
		date -= 1;
	}

	/* add offset to go from J2000 back to standard Julian date */
	date += POSTGRES_EPOCH_JDATE;

recalc_d:
	/* Julian day routine does not work for negative Julian days */
	if (date < 0 || date > (Timestamp) INT_MAX)
		return -1;

	j2date((int) date, &tm->tm_year, &tm->tm_mon, &tm->tm_mday);
recalc_t:
	dt2time(time, &tm->tm_hour, &tm->tm_min, &tm->tm_sec, fsec);

	*fsec = TSROUND(*fsec);
	/* roundoff may need to propagate to higher-order fields */
	if (*fsec >= 1.0)
	{
		time = ceil(time);
		if (time >= (double) SECS_PER_DAY)
		{
			time = 0;
			date += 1;
			goto recalc_d;
		}
		goto recalc_t;
	}
#endif

	/* Done if no TZ conversion wanted */
	if (tzp == NULL)
	{
		tm->tm_isdst = -1;
		tm->tm_gmtoff = 0;
		tm->tm_zone = NULL;
		if (tzn != NULL)
			*tzn = NULL;
		return 0;
	}

	/*
	 * If the time falls within the range of pg_time_t, use pg_localtime() to
	 * rotate to the local time zone.
	 *
	 * First, convert to an integral timestamp, avoiding possibly
	 * platform-specific roundoff-in-wrong-direction errors, and adjust to
	 * Unix epoch.  Then see if we can convert to pg_time_t without loss. This
	 * coding avoids hardwiring any assumptions about the width of pg_time_t,
	 * so it should behave sanely on machines without int64.
	 */
#ifdef HAVE_INT64_TIMESTAMP
	dt = (dt - *fsec) / USECS_PER_SEC +
		(POSTGRES_EPOCH_JDATE - UNIX_EPOCH_JDATE) * SECS_PER_DAY;
#else
	dt = rint(dt - *fsec +
			  (POSTGRES_EPOCH_JDATE - UNIX_EPOCH_JDATE) * SECS_PER_DAY);
#endif
	utime = (pg_time_t) dt;
	if ((Timestamp) utime == dt)
	{
		struct pg_tm *tx = pg_localtime(&utime, attimezone);

		tm->tm_year = tx->tm_year + 1900;
		tm->tm_mon = tx->tm_mon + 1;
		tm->tm_mday = tx->tm_mday;
		tm->tm_hour = tx->tm_hour;
		tm->tm_min = tx->tm_min;
		tm->tm_sec = tx->tm_sec;
		tm->tm_isdst = tx->tm_isdst;
		tm->tm_gmtoff = tx->tm_gmtoff;
		tm->tm_zone = tx->tm_zone;
		*tzp = -tm->tm_gmtoff;
		if (tzn != NULL)
			*tzn = tm->tm_zone;
	}
	else
	{
		/*
		 * When out of range of pg_time_t, treat as GMT
		 */
		*tzp = 0;
		/* Mark this as *no* time zone available */
		tm->tm_isdst = -1;
		tm->tm_gmtoff = 0;
		tm->tm_zone = NULL;
		if (tzn != NULL)
			*tzn = NULL;
	}

	return 0;
}
```

  * tm2timestamp

函数功能是把pg_tm结构转换成Timestamp，定义在src/backend/utils/adt/timestamp.c中1922行处，具体如下：

```
int
tm2timestamp(struct pg_tm * tm, fsec_t fsec, int *tzp, Timestamp *result)
{
	TimeOffset	date;
	TimeOffset	time;

	/* Julian day routines are not correct for negative Julian days */
	if (!IS_VALID_JULIAN(tm->tm_year, tm->tm_mon, tm->tm_mday))
	{
		*result = 0;			/* keep compiler quiet */
		return -1;
	}

	date = date2j(tm->tm_year, tm->tm_mon, tm->tm_mday) - POSTGRES_EPOCH_JDATE;
	time = time2t(tm->tm_hour, tm->tm_min, tm->tm_sec, fsec);

#ifdef HAVE_INT64_TIMESTAMP
	*result = date * USECS_PER_DAY + time;
	/* check for major overflow */
	if ((*result - time) / USECS_PER_DAY != date)
	{
		*result = 0;			/* keep compiler quiet */
		return -1;
	}
	/* check for just-barely overflow (okay except time-of-day wraps) */
	/* caution: we want to allow 1999-12-31 24:00:00 */
	if ((*result < 0 && date > 0) ||
		(*result > 0 && date < -1))
	{
		*result = 0;			/* keep compiler quiet */
		return -1;
	}
#else
	*result = date * SECS_PER_DAY + time;
#endif
	if (tzp != NULL)
		*result = dt2local(*result, -(*tzp));

	return 0;
}
```

  * EncodeDateTime

函数功能是把pg_tm结构根据时区信息编码成本地日期时间串，定义在src/backend/utils/adt/datetime.c中3956行处，具体如下：

```
void
EncodeDateTime(struct pg_tm * tm, fsec_t fsec, bool print_tz, int tz, const char *tzn, int style, char *str)
{
	int			day;

	Assert(tm->tm_mon >= 1 && tm->tm_mon <= MONTHS_PER_YEAR);

	/*
	 * Negative tm_isdst means we have no valid time zone translation.
	 */
	if (tm->tm_isdst < 0)
		print_tz = false;

	switch (style)
	{
		case USE_ISO_DATES:
		case USE_XSD_DATES:
			/* Compatible with ISO-8601 date formats */

			if (style == USE_ISO_DATES)
				sprintf(str, "%04d-%02d-%02d %02d:%02d:",
						(tm->tm_year > 0) ? tm->tm_year : -(tm->tm_year - 1),
						tm->tm_mon, tm->tm_mday, tm->tm_hour, tm->tm_min);
			else
				sprintf(str, "%04d-%02d-%02dT%02d:%02d:",
						(tm->tm_year > 0) ? tm->tm_year : -(tm->tm_year - 1),
						tm->tm_mon, tm->tm_mday, tm->tm_hour, tm->tm_min);

			AppendTimestampSeconds(str + strlen(str), tm, fsec);

			if (print_tz)
				EncodeTimezone(str, tz, style);

			if (tm->tm_year <= 0)
				sprintf(str + strlen(str), " BC");
			break;

		case USE_SQL_DATES:
			/* Compatible with Oracle/Ingres date formats */

			if (DateOrder == DATEORDER_DMY)
				sprintf(str, "%02d/%02d", tm->tm_mday, tm->tm_mon);
			else
				sprintf(str, "%02d/%02d", tm->tm_mon, tm->tm_mday);

			sprintf(str + 5, "/%04d %02d:%02d:",
					(tm->tm_year > 0) ? tm->tm_year : -(tm->tm_year - 1),
					tm->tm_hour, tm->tm_min);

			AppendTimestampSeconds(str + strlen(str), tm, fsec);

			/*
			 * Note: the uses of %.*s in this function would be risky if the
			 * timezone names ever contain non-ASCII characters.  However, all
			 * TZ abbreviations in the Olson database are plain ASCII.
			 */

			if (print_tz)
			{
				if (tzn)
					sprintf(str + strlen(str), " %.*s", MAXTZLEN, tzn);
				else
					EncodeTimezone(str, tz, style);
			}

			if (tm->tm_year <= 0)
				sprintf(str + strlen(str), " BC");
			break;

		case USE_GERMAN_DATES:
			/* German variant on European style */

			sprintf(str, "%02d.%02d", tm->tm_mday, tm->tm_mon);

			sprintf(str + 5, ".%04d %02d:%02d:",
					(tm->tm_year > 0) ? tm->tm_year : -(tm->tm_year - 1),
					tm->tm_hour, tm->tm_min);

			AppendTimestampSeconds(str + strlen(str), tm, fsec);

			if (print_tz)
			{
				if (tzn)
					sprintf(str + strlen(str), " %.*s", MAXTZLEN, tzn);
				else
					EncodeTimezone(str, tz, style);
			}

			if (tm->tm_year <= 0)
				sprintf(str + strlen(str), " BC");
			break;

		case USE_POSTGRES_DATES:
		default:
			/* Backward-compatible with traditional Postgres abstime dates */

			day = date2j(tm->tm_year, tm->tm_mon, tm->tm_mday);
			tm->tm_wday = j2day(day);

			memcpy(str, days[tm->tm_wday], 3);
			strcpy(str + 3, " ");

			if (DateOrder == DATEORDER_DMY)
				sprintf(str + 4, "%02d %3s", tm->tm_mday, months[tm->tm_mon - 1]);
			else
				sprintf(str + 4, "%3s %02d", months[tm->tm_mon - 1], tm->tm_mday);

			sprintf(str + 10, " %02d:%02d:", tm->tm_hour, tm->tm_min);

			AppendTimestampSeconds(str + strlen(str), tm, fsec);

			sprintf(str + strlen(str), " %04d",
					(tm->tm_year > 0) ? tm->tm_year : -(tm->tm_year - 1));

			if (print_tz)
			{
				if (tzn)
					sprintf(str + strlen(str), " %.*s", MAXTZLEN, tzn);
				else
				{
					/*
					 * We have a time zone, but no string version. Use the
					 * numeric form, but be sure to include a leading space to
					 * avoid formatting something which would be rejected by
					 * the date/time parser later. - thomas 2001-10-19
					 */
					sprintf(str + strlen(str), " ");
					EncodeTimezone(str, tz, style);
				}
			}

			if (tm->tm_year <= 0)
				sprintf(str + strlen(str), " BC");
			break;
	}
}
```

  * DecodeDateTime

函数功能与EncodeDateTime相反，定义在src/backend/utils/adt/datetime.c中行776处，具体如下：

```
int
DecodeDateTime(char **field, int *ftype, int nf,
			   int *dtype, struct pg_tm * tm, fsec_t *fsec, int *tzp)
{
	int			fmask = 0,
				tmask,
				type;
	int			ptype = 0;		/* "prefix type" for ISO y2001m02d04 format */
	int			i;
	int			val;
	int			dterr;
	int			mer = HR24;
	bool		haveTextMonth = FALSE;
	bool		isjulian = FALSE;
	bool		is2digits = FALSE;
	bool		bc = FALSE;
	pg_tz	   *namedTz = NULL;
	pg_tz	   *abbrevTz = NULL;
	pg_tz	   *valtz;
	char	   *abbrev = NULL;
	struct pg_tm cur_tm;

	/*
	 * We'll insist on at least all of the date fields, but initialize the
	 * remaining fields in case they are not set later...
	 */
	*dtype = DTK_DATE;
	tm->tm_hour = 0;
	tm->tm_min = 0;
	tm->tm_sec = 0;
	*fsec = 0;
	/* don't know daylight savings time status apriori */
	tm->tm_isdst = -1;
	if (tzp != NULL)
		*tzp = 0;

	for (i = 0; i < nf; i++)
	{
		switch (ftype[i])
		{
			case DTK_DATE:

				/*
				 * Integral julian day with attached time zone? All other
				 * forms with JD will be separated into distinct fields, so we
				 * handle just this case here.
				 */
				if (ptype == DTK_JULIAN)
				{
					char	   *cp;
					int			val;

					if (tzp == NULL)
						return DTERR_BAD_FORMAT;

					errno = 0;
					val = strtoint(field[i], &cp, 10);
					if (errno == ERANGE || val < 0)
						return DTERR_FIELD_OVERFLOW;

					j2date(val, &tm->tm_year, &tm->tm_mon, &tm->tm_mday);
					isjulian = TRUE;

					/* Get the time zone from the end of the string */
					dterr = DecodeTimezone(cp, tzp);
					if (dterr)
						return dterr;

					tmask = DTK_DATE_M | DTK_TIME_M | DTK_M(TZ);
					ptype = 0;
					break;
				}

				/*
				 * Already have a date? Then this might be a time zone name
				 * with embedded punctuation (e.g. "America/New_York") or a
				 * run-together time with trailing time zone (e.g. hhmmss-zz).
				 * - thomas 2001-12-25
				 *
				 * We consider it a time zone if we already have month & day.
				 * This is to allow the form "mmm dd hhmmss tz year", which
				 * we've historically accepted.
				 */
				else if (ptype != 0 ||
						 ((fmask & (DTK_M(MONTH) | DTK_M(DAY))) ==
						  (DTK_M(MONTH) | DTK_M(DAY))))
				{
					/* No time zone accepted? Then quit... */
					if (tzp == NULL)
						return DTERR_BAD_FORMAT;

					if (isdigit((unsigned char) *field[i]) || ptype != 0)
					{
						char	   *cp;

						if (ptype != 0)
						{
							/* Sanity check; should not fail this test */
							if (ptype != DTK_TIME)
								return DTERR_BAD_FORMAT;
							ptype = 0;
						}

						/*
						 * Starts with a digit but we already have a time
						 * field? Then we are in trouble with a date and time
						 * already...
						 */
						if ((fmask & DTK_TIME_M) == DTK_TIME_M)
							return DTERR_BAD_FORMAT;

						if ((cp = strchr(field[i], '-')) == NULL)
							return DTERR_BAD_FORMAT;

						/* Get the time zone from the end of the string */
						dterr = DecodeTimezone(cp, tzp);
						if (dterr)
							return dterr;
						*cp = '\0';

						/*
						 * Then read the rest of the field as a concatenated
						 * time
						 */
						dterr = DecodeNumberField(strlen(field[i]), field[i],
												  fmask,
												  &tmask, tm,
												  fsec, &is2digits);
						if (dterr < 0)
							return dterr;

						/*
						 * modify tmask after returning from
						 * DecodeNumberField()
						 */
						tmask |= DTK_M(TZ);
					}
					else
					{
						namedTz = pg_tzset(field[i]);
						if (!namedTz)
						{
							/*
							 * We should return an error code instead of
							 * ereport'ing directly, but then there is no way
							 * to report the bad time zone name.
							 */
							ereport(ERROR,
									(errcode(ERRCODE_INVALID_PARAMETER_VALUE),
									 errmsg("time zone \"%s\" not recognized",
											field[i])));
						}
						/* we'll apply the zone setting below */
						tmask = DTK_M(TZ);
					}
				}
				else
				{
					dterr = DecodeDate(field[i], fmask,
									   &tmask, &is2digits, tm);
					if (dterr)
						return dterr;
				}
				break;

			case DTK_TIME:

				/*
				 * This might be an ISO time following a "t" field.
				 */
				if (ptype != 0)
				{
					/* Sanity check; should not fail this test */
					if (ptype != DTK_TIME)
						return DTERR_BAD_FORMAT;
					ptype = 0;
				}
				dterr = DecodeTime(field[i], fmask, INTERVAL_FULL_RANGE,
								   &tmask, tm, fsec);
				if (dterr)
					return dterr;

				/*
				 * Check upper limit on hours; other limits checked in
				 * DecodeTime()
				 */
				/* test for > 24:00:00 */
				if (tm->tm_hour > HOURS_PER_DAY ||
					(tm->tm_hour == HOURS_PER_DAY &&
					 (tm->tm_min > 0 || tm->tm_sec > 0 || *fsec > 0)))
					return DTERR_FIELD_OVERFLOW;
				break;

			case DTK_TZ:
				{
					int			tz;

					if (tzp == NULL)
						return DTERR_BAD_FORMAT;

					dterr = DecodeTimezone(field[i], &tz);
					if (dterr)
						return dterr;
					*tzp = tz;
					tmask = DTK_M(TZ);
				}
				break;

			case DTK_NUMBER:

				/*
				 * Was this an "ISO date" with embedded field labels? An
				 * example is "y2001m02d04" - thomas 2001-02-04
				 */
				if (ptype != 0)
				{
					char	   *cp;
					int			val;

					errno = 0;
					val = strtoint(field[i], &cp, 10);
					if (errno == ERANGE)
						return DTERR_FIELD_OVERFLOW;

					/*
					 * only a few kinds are allowed to have an embedded
					 * decimal
					 */
					if (*cp == '.')
						switch (ptype)
						{
							case DTK_JULIAN:
							case DTK_TIME:
							case DTK_SECOND:
								break;
							default:
								return DTERR_BAD_FORMAT;
								break;
						}
					else if (*cp != '\0')
						return DTERR_BAD_FORMAT;

					switch (ptype)
					{
						case DTK_YEAR:
							tm->tm_year = val;
							tmask = DTK_M(YEAR);
							break;

						case DTK_MONTH:

							/*
							 * already have a month and hour? then assume
							 * minutes
							 */
							if ((fmask & DTK_M(MONTH)) != 0 &&
								(fmask & DTK_M(HOUR)) != 0)
							{
								tm->tm_min = val;
								tmask = DTK_M(MINUTE);
							}
							else
							{
								tm->tm_mon = val;
								tmask = DTK_M(MONTH);
							}
							break;

						case DTK_DAY:
							tm->tm_mday = val;
							tmask = DTK_M(DAY);
							break;

						case DTK_HOUR:
							tm->tm_hour = val;
							tmask = DTK_M(HOUR);
							break;

						case DTK_MINUTE:
							tm->tm_min = val;
							tmask = DTK_M(MINUTE);
							break;

						case DTK_SECOND:
							tm->tm_sec = val;
							tmask = DTK_M(SECOND);
							if (*cp == '.')
							{
								dterr = ParseFractionalSecond(cp, fsec);
								if (dterr)
									return dterr;
								tmask = DTK_ALL_SECS_M;
							}
							break;

						case DTK_TZ:
							tmask = DTK_M(TZ);
							dterr = DecodeTimezone(field[i], tzp);
							if (dterr)
								return dterr;
							break;

						case DTK_JULIAN:
							/* previous field was a label for "julian date" */
							if (val < 0)
								return DTERR_FIELD_OVERFLOW;
							tmask = DTK_DATE_M;
							j2date(val, &tm->tm_year, &tm->tm_mon, &tm->tm_mday);
							isjulian = TRUE;

							/* fractional Julian Day? */
							if (*cp == '.')
							{
								double		time;

								errno = 0;
								time = strtod(cp, &cp);
								if (*cp != '\0' || errno != 0)
									return DTERR_BAD_FORMAT;

#ifdef HAVE_INT64_TIMESTAMP
								time *= USECS_PER_DAY;
#else
								time *= SECS_PER_DAY;
#endif
								dt2time(time,
										&tm->tm_hour, &tm->tm_min,
										&tm->tm_sec, fsec);
								tmask |= DTK_TIME_M;
							}
							break;

						case DTK_TIME:
							/* previous field was "t" for ISO time */
							dterr = DecodeNumberField(strlen(field[i]), field[i],
													  (fmask | DTK_DATE_M),
													  &tmask, tm,
													  fsec, &is2digits);
							if (dterr < 0)
								return dterr;
							if (tmask != DTK_TIME_M)
								return DTERR_BAD_FORMAT;
							break;

						default:
							return DTERR_BAD_FORMAT;
							break;
					}

					ptype = 0;
					*dtype = DTK_DATE;
				}
				else
				{
					char	   *cp;
					int			flen;

					flen = strlen(field[i]);
					cp = strchr(field[i], '.');

					/* Embedded decimal and no date yet? */
					if (cp != NULL && !(fmask & DTK_DATE_M))
					{
						dterr = DecodeDate(field[i], fmask,
										   &tmask, &is2digits, tm);
						if (dterr)
							return dterr;
					}
					/* embedded decimal and several digits before? */
					else if (cp != NULL && flen - strlen(cp) > 2)
					{
						/*
						 * Interpret as a concatenated date or time Set the
						 * type field to allow decoding other fields later.
						 * Example: 20011223 or 040506
						 */
						dterr = DecodeNumberField(flen, field[i], fmask,
												  &tmask, tm,
												  fsec, &is2digits);
						if (dterr < 0)
							return dterr;
					}

					/*
					 * Is this a YMD or HMS specification, or a year number?
					 * YMD and HMS are required to be six digits or more, so
					 * if it is 5 digits, it is a year.  If it is six or more
					 * more digits, we assume it is YMD or HMS unless no date
					 * and no time values have been specified.  This forces 6+
					 * digit years to be at the end of the string, or to use
					 * the ISO date specification.
					 */
					else if (flen >= 6 && (!(fmask & DTK_DATE_M) ||
										   !(fmask & DTK_TIME_M)))
					{
						dterr = DecodeNumberField(flen, field[i], fmask,
												  &tmask, tm,
												  fsec, &is2digits);
						if (dterr < 0)
							return dterr;
					}
					/* otherwise it is a single date/time field... */
					else
					{
						dterr = DecodeNumber(flen, field[i],
											 haveTextMonth, fmask,
											 &tmask, tm,
											 fsec, &is2digits);
						if (dterr)
							return dterr;
					}
				}
				break;

			case DTK_STRING:
			case DTK_SPECIAL:
				/* timezone abbrevs take precedence over built-in tokens */
				type = DecodeTimezoneAbbrev(i, field[i], &val, &valtz);
				if (type == UNKNOWN_FIELD)
					type = DecodeSpecial(i, field[i], &val);
				if (type == IGNORE_DTF)
					continue;

				tmask = DTK_M(type);
				switch (type)
				{
					case RESERV:
						switch (val)
						{
							case DTK_CURRENT:
								ereport(ERROR,
									 (errcode(ERRCODE_FEATURE_NOT_SUPPORTED),
									  errmsg("date/time value \"current\" is no longer supported")));

								return DTERR_BAD_FORMAT;
								break;

							case DTK_NOW:
								tmask = (DTK_DATE_M | DTK_TIME_M | DTK_M(TZ));
								*dtype = DTK_DATE;
								GetCurrentTimeUsec(tm, fsec, tzp);
								break;

							case DTK_YESTERDAY:
								tmask = DTK_DATE_M;
								*dtype = DTK_DATE;
								GetCurrentDateTime(&cur_tm);
								j2date(date2j(cur_tm.tm_year, cur_tm.tm_mon, cur_tm.tm_mday) - 1,
									&tm->tm_year, &tm->tm_mon, &tm->tm_mday);
								break;

							case DTK_TODAY:
								tmask = DTK_DATE_M;
								*dtype = DTK_DATE;
								GetCurrentDateTime(&cur_tm);
								tm->tm_year = cur_tm.tm_year;
								tm->tm_mon = cur_tm.tm_mon;
								tm->tm_mday = cur_tm.tm_mday;
								break;

							case DTK_TOMORROW:
								tmask = DTK_DATE_M;
								*dtype = DTK_DATE;
								GetCurrentDateTime(&cur_tm);
								j2date(date2j(cur_tm.tm_year, cur_tm.tm_mon, cur_tm.tm_mday) + 1,
									&tm->tm_year, &tm->tm_mon, &tm->tm_mday);
								break;

							case DTK_ZULU:
								tmask = (DTK_TIME_M | DTK_M(TZ));
								*dtype = DTK_DATE;
								tm->tm_hour = 0;
								tm->tm_min = 0;
								tm->tm_sec = 0;
								if (tzp != NULL)
									*tzp = 0;
								break;

							default:
								*dtype = val;
						}

						break;

					case MONTH:

						/*
						 * already have a (numeric) month? then see if we can
						 * substitute...
						 */
						if ((fmask & DTK_M(MONTH)) && !haveTextMonth &&
							!(fmask & DTK_M(DAY)) && tm->tm_mon >= 1 &&
							tm->tm_mon <= 31)
						{
							tm->tm_mday = tm->tm_mon;
							tmask = DTK_M(DAY);
						}
						haveTextMonth = TRUE;
						tm->tm_mon = val;
						break;

					case DTZMOD:

						/*
						 * daylight savings time modifier (solves "MET DST"
						 * syntax)
						 */
						tmask |= DTK_M(DTZ);
						tm->tm_isdst = 1;
						if (tzp == NULL)
							return DTERR_BAD_FORMAT;
						*tzp -= val;
						break;

					case DTZ:

						/*
						 * set mask for TZ here _or_ check for DTZ later when
						 * getting default timezone
						 */
						tmask |= DTK_M(TZ);
						tm->tm_isdst = 1;
						if (tzp == NULL)
							return DTERR_BAD_FORMAT;
						*tzp = -val;
						break;

					case TZ:
						tm->tm_isdst = 0;
						if (tzp == NULL)
							return DTERR_BAD_FORMAT;
						*tzp = -val;
						break;

					case DYNTZ:
						tmask |= DTK_M(TZ);
						if (tzp == NULL)
							return DTERR_BAD_FORMAT;
						/* we'll determine the actual offset later */
						abbrevTz = valtz;
						abbrev = field[i];
						break;

					case AMPM:
						mer = val;
						break;

					case ADBC:
						bc = (val == BC);
						break;

					case DOW:
						tm->tm_wday = val;
						break;

					case UNITS:
						tmask = 0;
						ptype = val;
						break;

					case ISOTIME:

						/*
						 * This is a filler field "t" indicating that the next
						 * field is time. Try to verify that this is sensible.
						 */
						tmask = 0;

						/* No preceding date? Then quit... */
						if ((fmask & DTK_DATE_M) != DTK_DATE_M)
							return DTERR_BAD_FORMAT;

						/***
						 * We will need one of the following fields:
						 *	DTK_NUMBER should be hhmmss.fff
						 *	DTK_TIME should be hh:mm:ss.fff
						 *	DTK_DATE should be hhmmss-zz
						 ***/
						if (i >= nf - 1 ||
							(ftype[i + 1] != DTK_NUMBER &&
							 ftype[i + 1] != DTK_TIME &&
							 ftype[i + 1] != DTK_DATE))
							return DTERR_BAD_FORMAT;

						ptype = val;
						break;

					case UNKNOWN_FIELD:

						/*
						 * Before giving up and declaring error, check to see
						 * if it is an all-alpha timezone name.
						 */
						namedTz = pg_tzset(field[i]);
						if (!namedTz)
							return DTERR_BAD_FORMAT;
						/* we'll apply the zone setting below */
						tmask = DTK_M(TZ);
						break;

					default:
						return DTERR_BAD_FORMAT;
				}
				break;

			default:
				return DTERR_BAD_FORMAT;
		}

		if (tmask & fmask)
			return DTERR_BAD_FORMAT;
		fmask |= tmask;
	}							/* end loop over fields */

	/* do final checking/adjustment of Y/M/D fields */
	dterr = ValidateDate(fmask, isjulian, is2digits, bc, tm);
	if (dterr)
		return dterr;

	/* handle AM/PM */
	if (mer != HR24 && tm->tm_hour > HOURS_PER_DAY / 2)
		return DTERR_FIELD_OVERFLOW;
	if (mer == AM && tm->tm_hour == HOURS_PER_DAY / 2)
		tm->tm_hour = 0;
	else if (mer == PM && tm->tm_hour != HOURS_PER_DAY / 2)
		tm->tm_hour += HOURS_PER_DAY / 2;

	/* do additional checking for full date specs... */
	if (*dtype == DTK_DATE)
	{
		if ((fmask & DTK_DATE_M) != DTK_DATE_M)
		{
			if ((fmask & DTK_TIME_M) == DTK_TIME_M)
				return 1;
			return DTERR_BAD_FORMAT;
		}

		/*
		 * If we had a full timezone spec, compute the offset (we could not do
		 * it before, because we need the date to resolve DST status).
		 */
		if (namedTz != NULL)
		{
			/* daylight savings time modifier disallowed with full TZ */
			if (fmask & DTK_M(DTZMOD))
				return DTERR_BAD_FORMAT;

			*tzp = DetermineTimeZoneOffset(tm, namedTz);
		}

		/*
		 * Likewise, if we had a dynamic timezone abbreviation, resolve it
		 * now.
		 */
		if (abbrevTz != NULL)
		{
			/* daylight savings time modifier disallowed with dynamic TZ */
			if (fmask & DTK_M(DTZMOD))
				return DTERR_BAD_FORMAT;

			*tzp = DetermineTimeZoneAbbrevOffset(tm, abbrev, abbrevTz);
		}

		/* timezone not specified? then use session timezone */
		if (tzp != NULL && !(fmask & DTK_M(TZ)))
		{
			/*
			 * daylight savings time modifier but no standard timezone? then
			 * error
			 */
			if (fmask & DTK_M(DTZMOD))
				return DTERR_BAD_FORMAT;

			*tzp = DetermineTimeZoneOffset(tm, session_timezone);
		}
	}

	return 0;
}
```

引用
====

  * [https://zh.wikipedia.org/wiki/%E5%84%92%E7%95%A5%E6%97%A5](Julian-date)


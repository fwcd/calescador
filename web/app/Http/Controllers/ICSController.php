<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Jsvrcek\ICS\Model\Calendar as ICalendar;
use Jsvrcek\ICS\Model\CalendarEvent as ICalendarEvent;
use Jsvrcek\ICS\Utility\Formatter as ICalendarFormatter;
use Jsvrcek\ICS\CalendarStream as ICalendarStream;
use Jsvrcek\ICS\CalendarExport as ICalendarExport;

class ICSController extends Controller
{
    /** Fetches all calendar events in the iCalendar (.ics) format. */
    public function all()
    {
        // TODO: Factor out conversion methods

        $ical = new ICalendar();
        $ical->setProdId('-//calescador//calescador//EN');

        foreach (\App\Models\Event::get() as $event) {
            // TODO: Convert locations

            $icalEvent = new ICalendarEvent;
            $icalEvent
                ->setSummary($event->name)
                ->setStart($event->start_dt)
                ->setEnd($event->end_dt)
                ->setUid($event->id);
            $ical->addEvent($icalEvent);
        }

        // TODO: Attendees

        $icalExport = new ICalendarExport(new ICalendarStream, new ICalendarFormatter);
        $icalExport->addCalendar($ical);

        return $icalExport->getStream();
    }
}

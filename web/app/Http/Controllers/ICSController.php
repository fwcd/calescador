<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Jsvrcek\ICS\Model\Calendar as ICalendar;
use Jsvrcek\ICS\Model\CalendarEvent as ICalendarEvent;
use Jsvrcek\ICS\Model\Description\Location as ICalendarLocation;
use Jsvrcek\ICS\Model\Relationship\Attendee as ICalendarAttendee;
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

        foreach (\App\Models\Event::with('users')->get() as $event) {
            $icalLocation = new ICalendarLocation;
            $icalLocation->setName($event->location);

            $icalEvent = new ICalendarEvent;
            $icalEvent
                ->setSummary($event->name)
                ->setStart($event->start_dt)
                ->setEnd($event->end_dt)
                ->setUid($event->id)
                ->addLocation($icalLocation);

            foreach ($event->users as $user) {
                $icalAttendee = new ICalendarAttendee(new ICalendarFormatter);
                $icalAttendee
                    ->setName($user->name)
                    ->setParticipationStatus("ACCEPTED");
                $icalEvent->addAttendee($icalAttendee);
            }

            $ical->addEvent($icalEvent);
        }

        $icalExport = new ICalendarExport(new ICalendarStream, new ICalendarFormatter);
        $icalExport->addCalendar($ical);

        return $icalExport->getStream();
    }
}

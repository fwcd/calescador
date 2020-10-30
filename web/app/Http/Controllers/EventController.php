<?php

namespace App\Http\Controllers;

use App\Helpers\ValidationHelper;
use Illuminate\Http\Request;
use Validator;

class EventController extends Controller
{
    /** Fetches all calendar events. */
    public function all()
    {
        $events = \App\Models\Event::orderBy('start_dt', 'asc')->get();
        return response()->json($events);
    }

    /** Fetches upcoming calendar events. */
    public function upcoming()
    {
        $events = \App\Models\Event::orderBy('start_dt', 'asc')->where('start_dt', '>=', Carbon::now())->get();
        return response()->json($events);
    }

    /** Fetches an event by ID. */
    public function find($id)
    {
        $event = \App\Models\Event::findOrFail($id);
        return response()->json($event);
    }

    /** Fetches events by Discord message id. */
    public function findByDiscord($id)
    {
        $event = \App\Models\Event::where('discord_message_id', '=', $id)->firstOrFail();
        return response()->json($event);
    }

    /** Creates a new calendar event. */
    public function create(Request $request)
    {
        $validator = Validator::make($request->all(), [
            'name' => 'required|max:255',
            'start_dt' => 'required|date',
            'end_dt' => 'required|date|after:start_dt',
            'location' => 'max:255',
            'description' => 'max:2047',
            'discord_message_id' => 'max:127'
        ]);

        if ($validator->fails()) {
            return response()->json(ValidationHelper::validationError($validator), 400);
        }

        $event = new \App\Models\Event;
        $event->name = $request->name;
        $event->start_dt = $request->start_dt;
        $event->end_dt = $request->end_dt;
        $event->location = $request->location ?? '';
        $event->description = $request->description ?? '';
        $event->discord_message_id = $request->discord_message_id;
        $event->save();

        return response()->json($event, 201);
    }

    /** Deletes an existing calendar event by ID. */
    public function delete($id)
    {
        $event = \App\Models\Event::findOrFail($id);
        $event->delete();
        return response()->json("Successfully deleted event $id!", 200);
    }
}

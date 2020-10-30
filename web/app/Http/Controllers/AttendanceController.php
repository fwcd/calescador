<?php

namespace App\Http\Controllers;

use App\Helpers\ValidationHelper;
use Illuminate\Http\Request;
use Validator;

class AttendanceController extends Controller
{
    /** Creates a new attendance. */
    public function create($user_id, $event_id, Request $request)
    {
        $validator = Validator::make($request->all(), [
            'count' => 'required|max:127'
        ]);

        if ($validator->fails()) {
            return response()->json(ValidationHelper::validationError($validator), 400);
        }

        \App\Models\User::findOrFail($user_id)->events()->attach($event_id, ['count' => $request->count]);
        return response()->json("Successfully added attendance of $user_id to $event_id!", 200);
    }

    /** Fetches all attendances. */
    public function all()
    {
        $attendances = [];
        foreach (\App\Models\User::with('events')->get() as $user) {
            foreach ($user->events as $event) {
                array_push($attendances, $event->pivot);
            }
        }
        return response()->json($attendances, 200);
    }

    /** Fetches all attendances of a user. */
    public function findByUser($user_id)
    {
        $attendances = [];
        foreach (\App\Models\User::findOrFail($user_id)->events as $event) {
            array_push($attendances, $event->pivot);
        }
        return response()->json($attendances, 200);
    }

    /** Fetches a single attendance. */
    public function find($user_id, $event_id)
    {
        $attendance = \App\Models\User::findOrFail($user_id)->events()->findOrFail($event_id)->pivot;
        return response()->json($attendance, 200);
    }

    /** Deletes an attendance. */
    public function delete($user_id, $event_id)
    {
        \App\Models\User::findOrFail($user_id)->events()->detach($event_id);
        return response()->json("Successfully deleted attendance of $user_id to $event_id!", 200);
    }

}

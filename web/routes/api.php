<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use Carbon\Carbon;

/*
|--------------------------------------------------------------------------
| API Routes
|--------------------------------------------------------------------------
|
| Here is where you can register API routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| is assigned the "api" middleware group. Enjoy building your API!
|
*/

function validationError($validator) {
    $errorMessages = $validator->messages()->get('*');
    return Arr::first(Arr::flatten($errorMessages));
}

// TODO: Require authentication on all routes
// TODO: Factor out controllers

// Route::middleware('auth:api')->get('/user', function (Request $request) {

/** Fetches a list of all users. */
Route::get('/users', function (Request $request) {
    $users = App\Models\User::get();
    return response()->json($users);
});

/** Fetches a user by ID. */
Route::get('/users/{id}', function ($id) {
    $user = App\Models\User::findOrFail($id);
    return response()->json($user);
});

/** Fetches a user by Discord user ID. */
Route::get('/users/discord/{id}', function ($id) {
    $user = App\Models\User::where('discord_user_id', '=', $id)->firstOrFail();
    return response()->json($user);
});

/** Creates a new user. */
Route::post('/users', function (Request $request) {
    $validator = Validator::make($request->all(), [
        'name' => 'required|max:255',
        'password' => 'required'
    ]);

    if ($validator->fails()) {
        return response()->json(validationError($validator), 400);
    }

    $user = new App\Models\User;
    $user->name = $request->name;
    $user->password = Hash::make($request->password);
    $user->discord_user_id = $request->discord_user_id;
    $user->save();

    return response()->json($user, 201);
});

/** Deletes a user. */
Route::delete('/users/{id}', function ($id) {
    $user = App\Models\User::findOrFail($id);
    $user->delete();
    return response()->json("Successfully deleted user $id!", 200);
});

/** Fetch all calendar events. */
Route::get('/events', function () {
    $events = App\Models\Event::orderBy('start_dt', 'asc')->get();
    return response()->json($events);
});

/** Fetch upcoming calendar events. */
Route::get('/events/upcoming', function () {
    $events = App\Models\Event::orderBy('start_dt', 'asc')->where('start_dt', '>=', Carbon::now())->get();
    return response()->json($events);
});

/** Fetch an event by id. */
Route::get('/events/{id}', function ($id) {
    $event = App\Models\Event::findOrFail($id);
    return response()->json($event);
});

/** Fetch events by Discord message id. */
Route::get('/events/discord/{id}', function ($id) {
    $event = App\Models\Event::where('discord_message_id', '=', $id)->firstOrFail();
    return response()->json($event);
});

/** Create a new calendar event. */
Route::post('/events', function (Request $request) {
    $validator = Validator::make($request->all(), [
        'name' => 'required|max:255',
        'start_dt' => 'required|date',
        'end_dt' => 'required|date|after:start_dt',
        'location' => 'max:255',
        'description' => 'max:2047',
        'discord_message_id' => 'max:127'
    ]);

    if ($validator->fails()) {
        return response()->json(validationError($validator), 400);
    }

    $event = new App\Models\Event;
    $event->name = $request->name;
    $event->start_dt = $request->start_dt;
    $event->end_dt = $request->end_dt;
    $event->location = $request->location ?? '';
    $event->description = $request->description ?? '';
    $event->discord_message_id = $request->discord_message_id;
    $event->save();

    return response()->json($event, 201);
});

/** Delete an existing calendar event. */
Route::delete('/events/{id}', function ($id) {
    $event = App\Models\Event::findOrFail($id);
    $event->delete();
    return response()->json("Successfully deleted event $id!", 200);
});

/** Creates a new attendance. */
Route::put('/attendances/{user_id}/{event_id}', function ($user_id, $event_id, Request $request) {
    $validator = Validator::make($request->all(), [
        'count' => 'required|max:127'
    ]);

    if ($validator->fails()) {
        return response()->json(validationError($validator), 400);
    }

    App\Models\User::findOrFail($user_id)->events()->attach($event_id, ['count' => $request->count]);
    return response()->json("Successfully added attendance of $user_id to $event_id!", 200);
});

/** Fetches attendances. */
Route::get('/attendances', function (Request $request) {
    $attendances = [];
    foreach (App\Models\User::with('events')->get() as $user) {
        foreach ($user->events as $event) {
            array_push($attendances, $event->pivot);
        }
    }
    return response()->json($attendances, 200);
});

/** Fetches attendances of a user. */
Route::get('/attendances/{user_id}', function ($user_id, Request $request) {
    $attendances = [];
    foreach (App\Models\User::findOrFail($user_id)->events as $event) {
        array_push($attendances, $event->pivot);
    }
    return response()->json($attendances, 200);
});

/** Deletes an attendance. */
Route::delete('/attendances/{user_id}/{event_id}', function ($user_id, $event_id, Request $request) {
    App\Models\User::findOrFail($user_id)->users()->detach($event_id);
    return response()->json("Successfully deleted attendance of $user_id to $event_id!", 200);
});

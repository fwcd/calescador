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

// TODO: Require authentication on all routes

// Route::middleware('auth:api')->get('/user', function (Request $request) {

/** Fetches a list of all users. */
Route::get('/users', function (Request $request) {
    $users = App\Models\User::get();
    return response()->json($users);
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
    $event = App\Models\Event::where('discord_message_id', '==', $id)->firstOrFail();
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
        $errorMessages = $validator->messages()->get('*');
        $errorMessage = Arr::first(Arr::flatten($errorMessages));
        return response()->json($errorMessage, 400);
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

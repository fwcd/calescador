<?php

use App\Http\Controllers\EventController;
use App\Http\Controllers\UserController;
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
Route::get('/users', [UserController::class, 'all']);

/** Fetches a user by ID. */
Route::get('/users/{id}', [UserController::class, 'find']);

/** Fetches a user by Discord user ID. */
Route::get('/users/discord/{id}', [UserController::class, 'findByDiscord']);

/** Creates a new user. */
Route::post('/users', [UserController::class, 'create']);

/** Deletes a user. */
Route::delete('/users/{id}', [UserController::class, 'delete']);

/** Fetch all calendar events. */
Route::get('/events', [EventController::class, 'all']);

/** Fetch upcoming calendar events. */
Route::get('/events/upcoming', [EventController::class, 'upcoming']);

/** Fetch an event by id. */
Route::get('/events/{id}', [EventController::class, 'find']);

/** Fetch events by Discord message id. */
Route::get('/events/discord/{id}', [EventController::class, 'findByDiscord']);

/** Create a new calendar event. */
Route::post('/events', [EventController::class, 'create']);

/** Delete an existing calendar event. */
Route::delete('/events/{id}', [EventController::class, 'delete']);

/** Creates a new attendance. */
Route::put('/attendances/{user_id}/{event_id}', function ($user_id, $event_id, Request $request) {
    $validator = Validator::make($request->all(), [
        'count' => 'required|max:127'
    ]);

    if ($validator->fails()) {
        return response()->json(validationError($validator), 400);
    }

    \App\Models\User::findOrFail($user_id)->events()->attach($event_id, ['count' => $request->count]);
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

/** Fetches a single attendance. */
Route::get('/attendances/{user_id}/{event_id}', function ($user_id, $event_id, Request $request) {
    $attendance = \App\Models\User::findOrFail($user_id)->events()->findOrFail($event_id)->pivot;
    return response()->json($attendance, 200);
});

/** Deletes an attendance. */
Route::delete('/attendances/{user_id}/{event_id}', function ($user_id, $event_id, Request $request) {
    \App\Models\User::findOrFail($user_id)->events()->detach($event_id);
    return response()->json("Successfully deleted attendance of $user_id to $event_id!", 200);
});

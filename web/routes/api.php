<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;

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

Route::middleware('auth:api')->get('/user', function (Request $request) {
    return $request->user();
});

// TODO: Require authentication on all routes

/** Fetch all calendar events. */
Route::get('/events', function () {
    $events = App\Models\Event::orderBy('start_dt', 'asc')->get();

    return $events->toJson();
});

/** Create a new calendar event. */
Route::post('/events', function (Request $request) {
    $validator = Validator::make($request->all(), [
        'name' => 'required|max:255',
        'start_dt' => 'required|date',
        'end_dt' => 'required|date|after:start_dt',
        'location' => 'max:255',
        'description' => 'max:2047'
    ]);

    if ($validator->fails()) {
        $errorMessages = $validator->messages()->get('*');
        $errorMessage = Arr::first(Arr::flatten($errorMessages));
        return response("$errorMessage\n", 400);
    }

    $event = new App\Models\Event;
    $event->name = $request->name;
    $event->start_dt = $request->start_dt;
    $event->end_dt = $request->end_dt;
    $event->location = $request->location ?? '';
    $event->description = $request->description ?? '';
    $event->save();

    return response("Successfully created event!\n", 201);
});

/** Delete an existing calendar event. */
Route::delete('/events/{id}', function ($id) {
    // TODO
});

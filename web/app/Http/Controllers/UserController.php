<?php

namespace App\Http\Controllers;

use App\Helpers\ValidationHelper;
use Illuminate\Http\Request;

class UserController extends Controller
{
    // TODO: Auth in constructor

    /** Fetches a list of all users. */
    public function all(Request $request)
    {
        $users = \App\Models\User::get();
        return response()->json($users);
    }

    /** Fetches a user by ID. */
    public function find($id)
    {
        $user = \App\Models\User::findOrFail($id);
        return response()->json($user);
    }

    /** Fetches a user by Discord user ID. */
    public function findByDiscord($id)
    {
        $user = \App\Models\User::where('discord_user_id', '=', $id)->firstOrFail();
        return response()->json($user);
    }

    /** Creates a new user. */
    public function create(Request $request)
    {
        $validator = Validator::make($request->all(), [
            'name' => 'required|max:255',
            'password' => 'required'
        ]);

        if ($validator->fails()) {
            return response()->json(ValidationHelper::validationError($validator), 400);
        }

        $user = new \App\Models\User;
        $user->name = $request->name;
        $user->password = Hash::make($request->password);
        $user->discord_user_id = $request->discord_user_id;
        $user->save();

        return response()->json($user, 201);
    }

    /** Deletes a user by ID. */
    public function delete($id)
    {
        $user = \App\Models\User::findOrFail($id);
        $user->delete();
        return response()->json("Successfully deleted user $id!", 200);
    }
}

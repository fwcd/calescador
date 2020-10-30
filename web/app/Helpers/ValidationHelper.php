<?php

namespace App\Helpers\ValidationHelper;

class ValidationHelper
{
    public static function validationError($validator)
    {
        $errorMessages = $validator->messages()->get('*');
        return Arr::first(Arr::flatten($errorMessages));
    }
}

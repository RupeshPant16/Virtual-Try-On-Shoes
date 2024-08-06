using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SwitchCharacterScript : MonoBehaviour
{

	// referenses to controlled game objects
	public GameObject Avatar1, Avatar2, Avatar3;

	// variable contains which avatar is on and active
	int whichAvatarIsOn = 1;

	// Use this for initialization
	void Start()
	{

		// anable first avatar and disable another one
		Avatar1.gameObject.SetActive(true);
		Avatar2.gameObject.SetActive(false);
		Avatar3.gameObject.SetActive(false);

	}

	// public method to switch avatars by pressing UI button
	public void SwitchAvatar()
	{

		// processing whichAvatarIsOn variable
		switch (whichAvatarIsOn)
		{

			// if the first avatar is on
			case 1:

				// then the second avatar is on now
				whichAvatarIsOn = 2;

				// disable the first one and anable the second one
				Avatar1.gameObject.SetActive(false);
				Avatar2.gameObject.SetActive(true);
				Avatar3.gameObject.SetActive(false);
				break;

			// if the second avatar is on
			case 2:

				// then the first avatar is on now
				whichAvatarIsOn = 3;

				// disable the second one and third one and enable the first one
				Avatar1.gameObject.SetActive(false);
				Avatar2.gameObject.SetActive(false);
				Avatar3.gameObject.SetActive(true);
				break;

			case 3:

				// then the first avatar is on now
				whichAvatarIsOn = 1;

				// disable the second one and third one and enable the first one
				Avatar1.gameObject.SetActive(true);
				Avatar2.gameObject.SetActive(false);
				Avatar3.gameObject.SetActive(false);
				break;

		}

	}
}
